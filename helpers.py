from z3 import If, IntVal, BV2Int, Abs, BitVecs

from constants import BIT_VECTOR_LENGTH, ONE
from def_exc.utils import numbits


def Max(x, y):
    return If(x > y, x, y)

def Min(x, y):
    return If(x > y, y, x)

def min_val_bit_constrained(n):
    res = -BV2Int(ONE << numbits(Abs(n)-1))
    return If(n == 0, IntVal(-1), res)

def max_val_bit_constrained(n):
    x = If(n < 0, Abs(n) - 1, n)
    return (ONE << numbits(Abs(x)))-1

def initialize_interval(s, x, name="x"):
    lx, ux = BitVecs(f'l{name} u{name}', BIT_VECTOR_LENGTH)

    x_int= BV2Int(x, True)
    s.add(BV2Int(lx, True) <= x_int, x_int <= BV2Int(ux, True))

    return lx, ux