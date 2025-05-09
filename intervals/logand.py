from datetime import MAXYEAR

from z3 import Solver, BitVecs, BV2Int, unsat, Not, And, Ints

from constants import BIT_VECTOR_LENGTH
from helpers import min_val_bit_constrained, Min, Max
from helpers import initialize_interval


def test_logand_unsigned():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    ux, uy = Ints("ux uy")
    x_int, y_int = BV2Int(x), BV2Int(y)

    s.add(x_int <= ux, y_int <= uy, Not(BV2Int(x & y) <= Min(ux, uy)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_both_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(lx >= 0, ly >= 0)

    con = BV2Int(x & y, True)
    lower = 0
    upper = Min(BV2Int(ux, True), BV2Int(uy, True))

    s.add(Not(And( lower <= con, con <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_both_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(ux < 0, uy < 0)

    con = BV2Int(x & y, True)
    lower = min_val_bit_constrained(Min(lx, ly))
    upper = 0

    s.add(Not(And(lower <= con, con <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_non_negative_and_unknown():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(lx >= 0, ly < 0)

    con = BV2Int(x & y, True)
    lower = 0
    upper = BV2Int(ux, True)

    s.add(Not(And(lower <= con, con <= upper)))

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_otherwise():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")

    con = BV2Int(x & y, True)
    lower = min_val_bit_constrained(Min(lx, ly))
    upper = Max(BV2Int(ux, True), BV2Int(uy, True))
    s.add(Not(And(lower <= con, con <= upper)))

    assert s.check() == unsat, f'Counterexample: {s.model()}'