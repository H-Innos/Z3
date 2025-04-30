from z3 import If, Abs, BV2Int
from constants import ONE

def Max(x, y):
    return If(x > y, x, y)

def Min(x, y):
    return If(x > y, y, x)

def get_int_bound_from_bits(bits):
    return If(BV2Int(bits, True) >= 0, BV2Int(ONE << bits, True), -BV2Int(ONE << Abs(bits)), True)

def next_power_of_2(n):
    x = n - 1
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    return If(n <= 0, 1, x + 1)