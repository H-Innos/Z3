from z3 import If, Abs, BV2Int, IntVal, BitVecVal, Extract
from constants import ONE, ZERO, BIT_VECTOR_LENGTH


def Max(x, y):
    return If(x > y, x, y)

def Min(x, y):
    return If(x > y, y, x)

def get_int_bound_from_bits(bits):
    return If(BV2Int(bits, True) >= 0,
              If(BV2Int(bits, True) == 0,
                 IntVal(0),
                 BV2Int(ONE << bits, True)
                 ),
              -BV2Int(ONE << Abs(bits)), True)

def min_val_bit_constrained(n):
    abs_n = (n ^ (n >> BitVecVal(BIT_VECTOR_LENGTH - 1, BIT_VECTOR_LENGTH))) - (n >> BitVecVal(BIT_VECTOR_LENGTH - 1, BIT_VECTOR_LENGTH))

    abs_n |= abs_n >> 1
    abs_n |= abs_n >> 2
    abs_n |= abs_n >> 4
    abs_n |= abs_n >> 8
    abs_n |= abs_n >> 16
    abs_n |= abs_n >> 32

    return If(abs_n <= 1, -1, abs_n)

def numbits(x):
    size = x.size()
    result = BitVecVal(0, size)
    for i in range(size):
        result = If(Extract(i, i, x) == BitVecVal(1, 1), BitVecVal(i + 1, size), result)
    return result



def max_val_bit_constrained(n):
    if n < 0:
        abs_n = -n - 1
    else:
        abs_n = n

    x = BitVecVal(1, BIT_VECTOR_LENGTH)

    while x.as_long() <= abs_n:
        x = x << 1

    return (x - 1).as_long()

def next_power_of_2(n):
    x = n-1
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    x |= x >> 32
    return  If(n <= 0, 1, x + 1)