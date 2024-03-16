import math
import os

def uniform_dist():
    return int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)

def exp_dist(lumb):
    uniform = uniform_dist()
    y = math.log( (1 - uniform) / lumb ) / ( -lumb )
    return y

def pois_dist(lumb):
    uniform = uniform_dist()
    F_pois = 1 / math.exp(lumb)
    value = 0
    factorial = 1
    while(uniform > F_pois):
        value += 1
        factorial *= value
        F_pois += (lumb ** value) / (factorial) * ( 1 / math.exp(lumb) )
    return value
s = 0
for i in range(100):
    if pois_dist(0.02) == 1:
        s +=1
print(s)