class result_values():

    def __init__(self, lim_distribution = [], P_rej = 0, P_queue = 0,
                 Q = 0, A = 0, L_hand = 0, L_queue = 0, L_system = 0,
                 T_queue = 0, T_hand = 0, T_system = 0):

        self.lim_distribution = lim_distribution
        self.P_rej = P_rej
        self.P_queue = P_queue
        self.Q = Q
        self.A = A
        self.L_hand = L_hand
        self.L_queue = L_queue
        self.L_system = L_system
        self.T_queue = T_queue
        self.T_hand = T_hand
        self.T_system = T_system

    def __str__(self):

        return "Distribution = "+ str(self.lim_distribution) + '\n' +\
            "P_rej = " + str(self.P_rej) + '\n' +\
            "P_queue = " + str(self.P_queue) + '\n' +\
            "Q = " + str(self.Q) + '\n' +\
            "A = " + str(self.A) + '\n' +\
            "L_hand = " + str(self.L_hand) + '\n' +\
            "L_queue = " + str(self.L_queue) + '\n' +\
            "L_system = " + str(self.L_system) + '\n' +\
            "T_queue = " + str(self.T_queue) + '\n' +\
            "T_hand = " + str(self.T_hand) + '\n' +\
            "T_system = " + str(self.T_system)


def calculate_theoretic_values(lumb, nu, N):

    p = lumb / nu

    if p != 1:
        lim_distribution = []
        lim_distribution.append( (1 - p) / ( 1 - p ** (N + 2) ) )
        for i in range(1, N+2):
            lim_distribution.append( lim_distribution[i-1] * p )
        P_rej = lim_distribution[N+1]
        P_queue = ( p ** 2 ) * (1 - p ** N) / (1 - p ** ( N + 2 ) )
        Q = 1 - P_rej
        A = lumb * Q
        L_hand = 1 - lim_distribution[0]
        L_queue = lim_distribution[0] * ( p ** 2 ) * ( 1 - ( p ** N ) * ( N + 1 - N * p) ) / ( ( 1 - p ) ** 2 )
        L_system = L_hand + L_queue

    else:

        lim_distribution = [1 / ( N + 2 )] * ( N + 2 )
        P_rej = 1 / ( N + 2 )
        P_queue = N / ( N + 2 )
        Q = 1 - P_rej
        A = lumb * Q
        L_hand = ( N + 1 ) / ( N + 2 )
        L_queue = N * ( N + 1 ) / ( 2 * ( N + 2 ) )
        L_system = ( N + 1 ) / 2

    T_queue = L_queue / lumb
    T_hand = L_hand / lumb
    T_system = L_system / lumb

    return result_values(lim_distribution, P_rej, P_queue, Q, A, L_hand, L_queue, \
                         L_system, T_queue, T_hand, T_system)

print(calculate_theoretic_values(4, 6, 10))