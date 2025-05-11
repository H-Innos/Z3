from z3 import Solver, BitVecs, BV2Int, unsat, Not, And

from constants import BIT_VECTOR_LENGTH
from helpers import Max, Min, max_val_bit_constrained
from helpers import initialize_interval


def test_logor_both_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(lx >= 0, ly >= 0)

    dis = BV2Int(x | y, True)
    lower = Max(BV2Int(lx, True), BV2Int(ly, True))
    upper = BV2Int(max_val_bit_constrained(Max(ux, uy)), True)

    s.add(Not(And(lower <= dis,dis <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_both_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(ux < 0, uy < 0)

    dis = BV2Int(x | y, True)
    lower = BV2Int(Max(lx, ly), True)
    upper = 0

    s.add(Not(And(lower <= dis,dis <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_neg_and_either():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")
    s.add(ux < 0, uy >= 0)

    dis = BV2Int(x | y, True)
    lower = BV2Int(lx, True)
    upper = 0

    s.add(Not(And(lower <= dis, dis <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_otherwise():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)
    ly, uy = initialize_interval(s, y, "y")

    dis = BV2Int(x | y, True)
    lower = BV2Int(Min(lx, ly), True)
    upper = BV2Int(max_val_bit_constrained(Max(ux, uy)), True)

    s.add(Not(And(lower <= dis, dis <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'