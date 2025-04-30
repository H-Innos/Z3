from helpers import Max, Min
from z3 import If

def interval_meet(i1, i2):
    lower = Max(i1[0], i2[0])
    upper = Min(i1[1], i2[1])

    return lower, upper

def interval_join(i1, i2):
    lower = Min(i1[0], i2[0])
    upper = Max(i2[1], i2[1])

    return lower, upper
