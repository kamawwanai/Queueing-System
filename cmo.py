from PyQt6.QtCore import  pyqtSignal, QObject

import distributions
import theory_calc
import queue

params = {'lumb': 4, 'nu': 6, 'N': 10, 'max_time': 500000}
timestep = 0.01

class System(QObject):

    request_cancelled = pyqtSignal(str)
    request_in_queue = pyqtSignal(str)
    request_in_handler = pyqtSignal(str)
    request_has_proccesed = pyqtSignal(str)

    def __init__(self, params):
        super().__init__()

        self.values = theory_calc.result_values()
        self.req_queue = queue.Queue()
        self.time = 0
        self.count_of_timesteps = 0
        self.count_of_reqs_in_system = 0
        self.count_of_rejections = 0
        self.count_of_all_reqs = 0
        self.count_of_reqs_after_queue = 0
        self.handler_timer = 0
        self.lumb = params['lumb']
        self.nu = params['nu']
        self.N = params['N']
        self.max_time = params['max_time']
        self.values.lim_distribution = [0] * (self.N + 2)

    def __iter__(self):

        return self

    def __next__(self):

        if self.time >= self.max_time:
            raise StopIteration

        self.time += timestep
        self.count_of_timesteps += 1


        if distributions.pois_dist(self.lumb * timestep) != 0:

            self.count_of_all_reqs += 1

            if self.count_of_reqs_in_system < self.N + 1:
                self.get_req()
            else:
                self.count_of_rejections += 1
                self.values.P_rej = self.count_of_rejections / self.count_of_all_reqs
                self.count_of_reqs_after_queue += 1
                self.values.T_queue = (self.values.T_queue * (
                            self.count_of_reqs_after_queue - 1)) / self.count_of_reqs_after_queue
                self.values.T_hand = (self.values.T_hand * (self.count_of_all_reqs - self.count_of_reqs_in_system) )\
                                       / (self.count_of_all_reqs - self.count_of_reqs_in_system + 1)
                # запрос отклонен
                self.request_cancelled.emit("Запрос отклонен")


            self.values.Q = ( self.count_of_all_reqs - self.count_of_rejections ) / self.count_of_all_reqs


        self.values.A = ( self.count_of_all_reqs - self.count_of_rejections ) / self.time


        if self.count_of_reqs_in_system - 1 >= 0:

            self.values.L_hand = ( self.values.L_hand * ( self.time - timestep ) + timestep) / self.time

            if distributions.pois_dist(self.nu * timestep) != 0:
                self.handle_req()

        else:
            self.values.L_hand = ( self.values.L_hand * ( self.time - timestep ) ) / self.time

        if self.count_of_reqs_in_system - 1 >= 0:

            self.values.L_queue = ( self.values.L_queue * ( self.time - timestep ) + timestep * ( self.count_of_reqs_in_system - 1) ) / self.time

        else:
            self.values.L_queue = self.values.L_queue * (self.time - timestep) / self.time

        self.values.L_system = (self.values.L_system * (self.time - timestep) + timestep * self.count_of_reqs_in_system ) / self.time
        self.values.T_system = self.values.T_hand + self.values.T_queue

        self.update_distributions(self.count_of_reqs_in_system)

        if self.count_of_reqs_in_system > 1:
            self.values.P_queue = ( self.values.P_queue * (self.count_of_timesteps - 1) + 1 ) / self.count_of_timesteps
        else:
            self.values.P_queue = (self.values.P_queue * (self.count_of_timesteps - 1) ) / self.count_of_timesteps




    def get_req(self):
        self.count_of_reqs_in_system += 1

        self.values.P_rej = self.values.P_rej * ( self.count_of_all_reqs - 1 ) / self.count_of_all_reqs

        if  self.count_of_reqs_in_system == 1:
            self.handler_timer = self.time
            self.count_of_reqs_after_queue += 1
            self.values.T_queue = ( self.values.T_queue * ( self.count_of_reqs_after_queue - 1 ) ) / self.count_of_reqs_after_queue
            # запрос помещен в обработчик
            self.request_in_handler.emit("Запрос помещен в обработчик")
        else:
            self.req_queue.put(self.time)
            # запрос пришел в очередь
            self.request_in_queue.emit("Запрос пришел в очередь")


    def handle_req(self):

        time_in_handler = self.time - self.handler_timer
        self.values.T_hand = ( self.values.T_hand * ( self.count_of_all_reqs - self.count_of_reqs_in_system ) \
                               + time_in_handler ) / ( self.count_of_all_reqs - self.count_of_reqs_in_system + 1)
        self.count_of_reqs_in_system -= 1

        # запрос обработался
        self.request_has_proccesed.emit("Запрос обработался")

        if self.count_of_reqs_in_system != 0:

            self.count_of_reqs_after_queue += 1
            start_time = self.req_queue.get()
            self.handler_timer = self.time

            time_in_queue = self.time - start_time
            self.values.T_queue = ( self.values.T_queue * ( self.count_of_reqs_after_queue - 1 ) + time_in_queue ) / self.count_of_reqs_after_queue
            # запрос помещен в обработчик
            self.request_in_handler.emit("Запрос помещен в обработчик")





    def update_distributions(self, state):
        for index in range(len(self.values.lim_distribution)):
            if index == state:
                self.values.lim_distribution[index] = ( self.values.lim_distribution[index] * ( self.count_of_timesteps - 1 ) + 1 ) / self.count_of_timesteps
            else:
                self.values.lim_distribution[index] = ( self.values.lim_distribution[index] * ( self.count_of_timesteps - 1 ) ) / self.count_of_timesteps



cmo = System(params)
cmo_iter = cmo.__iter__()
for i in range(int((200 / timestep))):
    next(cmo_iter)

print(cmo.values)
'''for i in range(100):
    cmo = System(params)
    cmo_iter = cmo.__iter__()
    for i in range(int((1000 / timestep))):
        next(cmo_iter)
    print(cmo.values.P_queue)'''