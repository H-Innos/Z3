from z3 import Solver, BitVecs, BV2Int, Not, And, unsat, Abs, BitVecVal, IntVal

from constants import BIT_VECTOR_LENGTH
from helpers import max_val_bit_constrained, Max, Min, min_val_bit_constrained
from helpers import initialize_interval


def test_logxor_both_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(lx >= 0, ly >= 0)

    xor = BV2Int(x ^ y, True)
    lower = 0
    upper = BV2Int(max_val_bit_constrained(Max(ux, uy)), True)

    s.add(Not(And(lower <= xor, xor <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logxor_both_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(ux < 0, uy < 0)

    xor = BV2Int(x ^ y, True)
    lower = 0
    upper = BV2Int(max_val_bit_constrained(Min(lx, ly)), True)

    s.add(Not(And(lower <= xor, xor <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model().eval(upper)}'

def test_logxor_negative_and_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(lx >= 0, uy < 0)

    xor = BV2Int(x ^ y, True)
    lower = Min(Min(min_val_bit_constrained(Abs(lx)+1), min_val_bit_constrained(Abs(ux)+1)), Min(min_val_bit_constrained(Abs(ly)+1), min_val_bit_constrained(Abs(uy)+1)))
    upper = 0

    s.add(Not(And(lower <= xor, xor <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logxor_otherwise():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")

    xor = BV2Int(x ^ y, True)
    lower = Min(Min(min_val_bit_constrained(lx),min_val_bit_constrained(ly)),
                Min(BV2Int(-max_val_bit_constrained(ux)-1, True),BV2Int(-max_val_bit_constrained(uy)-1, True)))
    upper = BV2Int(Max(Max(max_val_bit_constrained(lx), max_val_bit_constrained(ux)), Max(max_val_bit_constrained(ly), max_val_bit_constrained(uy))), True)

    s.add(Not(And(lower <= xor, xor <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'