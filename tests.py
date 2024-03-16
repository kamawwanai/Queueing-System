import cmo
import theory_calc

#Distribution
#P_rej
#P_queue
#Q
#A
#L_hand
#L_queue
#L_system
#T_queue
#T_hand
#T_system
error = 0.15

p = {'lumb': 1, 'nu': 9, 'N': 1, 'max_time': 500000}

a = theory_calc.calculate_theoretic_values(1, 1, 1)


z = cmo.System(p)
cmo_iter = z.__iter__()
for i in range(int((50 / 0.01))):
    next(cmo_iter)

print('fewsfsf', z.values)


N_values = list(range(1, 11, 2))
lumb_values = list(range(1, 11, 2))
nu_values = list(range(1, 11, 2))

count_itterations = 0

Distribution_count = 0
len_D = 0

P_rej_count = 0
P_queue_count = 0
Q_count = 0
A_count = 0
L_hand_count = 0
L_queue_count = 0
L_system_count = 0
T_queue_count = 0
T_hand_count = 0
T_system_count = 0

for N in N_values:
    for lumb in lumb_values:
        for nu in nu_values:
            params = {'lumb': lumb, 'nu': nu, 'N': N, 'max_time': 500000}

            Z = cmo.System(params)

            cmo_iter = Z.__iter__()
            for i in range(int((200 / 0.01))):
                next(cmo_iter)
            a = theory_calc.calculate_theoretic_values(lumb, nu, N) ## В a - все значения theory
            z = Z.values ## В z - Все значения cmo

            count_itterations += 1

            for j in range(N):
                if z.lim_distribution[j] - a.lim_distribution[j] > 0.1:
                    if abs(float(z.lim_distribution[j]) - float(a.lim_distribution[j])) < float(a.lim_distribution[j]) * error:
                        Distribution_count += 1
                else:
                    if abs(float(z.lim_distribution[j]) - float(a.lim_distribution[j])) < 0.01:
                        Distribution_count += 1

            len_D += N
            if a.P_rej >= 0.1:
                if abs(float(z.P_rej) - float(a.P_rej)) <= float(a.P_rej) * error:
                    P_rej_count += 1
            else:
                if abs(float(z.P_rej) - float(a.P_rej)) <= 0.01:
                    P_rej_count += 1

            if a.P_queue >= 0.1:
                if abs(float(z.P_queue) - float(a.P_queue)) <= float(a.P_queue) * error:
                    P_queue_count += 1
            else:
                if abs(float(z.P_queue) - float(a.P_queue)) <= 0.01:
                    P_queue_count += 1

            if abs(float(z.Q) - float(a.Q)) <= float(a.Q) * error:
                Q_count += 1

            if abs(float(z.A) - float(a.A)) <= float(a.A) * error:
                A_count += 1

            if abs(float(z.L_hand) - float(a.L_hand)) <= float(a.L_hand) * error:
                L_hand_count += 1

            if abs(float(z.L_queue) - float(a.L_queue)) <= float(a.L_queue) * error:
                L_queue_count += 1

            if abs(float(z.L_system) - float(a.L_system)) <= float(a.L_system) * error:
                L_system_count += 1

            if abs(float(z.T_queue) - float(a.T_queue)) <= float(a.T_queue) * error:
                T_queue_count += 1

            if abs(float(z.T_hand) - float(a.T_hand)) <= float(a.T_hand) * error:
                T_hand_count += 1

            if abs(float(z.T_system) - float(a.T_system)) <= float(a.T_system) * error:
                T_system_count += 1
            print(count_itterations)





print(Distribution_count/len_D)

print(f"P_rej доля: {P_rej_count/count_itterations}")
print(f"P_queue доля: {P_queue_count/count_itterations}")
print(f"Q доля: {Q_count/count_itterations}")
print(f"A доля: {A_count/count_itterations}")
print(f"L_hand доля: {L_hand_count/count_itterations}")
print(f"L_queue доля: {L_queue_count/count_itterations}")
print(f"L_system доля: {L_system_count/count_itterations}")
print(f"T_queue доля: {T_queue_count/count_itterations}")
print(f"T_hand доля: {T_hand_count/count_itterations}")
print(f"T_system доля: {T_system_count/count_itterations}")
