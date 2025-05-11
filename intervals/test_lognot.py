from z3 import BitVec, Solver, BV2Int, unsat, Not, And

from constants import BIT_VECTOR_LENGTH
from helpers import initialize_interval


def test_lognot():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    lx, ux = initialize_interval(s, x)

    neg = BV2Int(~x, True)
    lower = BV2Int(~ux, True)
    upper = BV2Int(~lx, True)

    s.add(Not(And(lower <= neg, neg <= upper)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'