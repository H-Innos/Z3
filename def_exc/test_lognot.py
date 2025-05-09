from z3 import Solver, BitVec, BV2Int, unsat, Not, And

from constants import BIT_VECTOR_LENGTH
from def_exc.utils import initialize_bit_interval, get_int_bound_from_bits


def test_lognot_exc():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    neg = BV2Int(~x, True)

    lower_int = get_int_bound_from_bits(-x_upper_bit_range)
    upper_int = get_int_bound_from_bits(-x_lower_bit_range)

    s.add(Not(And(
        neg >= lower_int,
        neg <= upper_int
    )))

    assert s.check() == unsat, f'Counterexample: {s.model()}'
