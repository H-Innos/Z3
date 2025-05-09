from z3 import If, IntVal, BV2Int, Abs, BitVecs, BitVecVal, Extract

from constants import BIT_VECTOR_LENGTH, ONE

# Z3 SHORTCUTS
def Max(x, y):
    return If(x > y, x, y)

def Min(x, y):
    return If(x > y, y, x)
# ----------

# BIT VECTOR FUNCTIONS
def numbits(x):
    result = BitVecVal(0, BIT_VECTOR_LENGTH)
    for i in range(BIT_VECTOR_LENGTH):
        result = If(Extract(i, i, x) == BitVecVal(1, 1), BitVecVal(i + 1, BIT_VECTOR_LENGTH), result)
    return result

def min_val_bit_constrained(n):
    res = -BV2Int(ONE << numbits(Abs(n)-1))
    return If(n == 0, IntVal(-1), res)

def max_val_bit_constrained(n):
    x = If(n < 0, Abs(n) - 1, n)
    return (ONE << numbits(Abs(x)))-1
# ----------

# PROOF SETUP FUNCTION
def initialize_interval(s, x, name="x"):
    lx, ux = BitVecs(f'l{name} u{name}', BIT_VECTOR_LENGTH)

    x_int= BV2Int(x, True)
    s.add(BV2Int(lx, True) <= x_int, x_int <= BV2Int(ux, True))

    return lx, ux
# ----------

# INTERVAL OPERATIONS
def interval_meet(i1, i2):
    lower = Max(i1[0], i2[0])
    upper = Min(i1[1], i2[1])
    return lower, upper

def interval_join(i1, i2):
    lower = Min(i1[0], i2[0])
    upper = Max(i1[1], i2[1])
    return lower, upper