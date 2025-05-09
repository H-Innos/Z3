from z3 import Solver, BitVec, BitVecs, BV2Int, unsat, Not, And, Abs, BitVecVal

from constants import BIT_VECTOR_LENGTH
from def_exc.utils import initialize_bit_interval, get_int_bound_from_bits
from helpers import Max, interval_join, numbits


def test_logor_exc_exc():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x, "x")
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")

    join_lower, join_upper = interval_join([x_lower_bit_range, x_upper_bit_range], [y_lower_bit_range, y_upper_bit_range])

    join_lower_int = get_int_bound_from_bits(join_lower)
    join_upper_int = get_int_bound_from_bits(join_upper)

    dis = BV2Int(x | y, True)
    s.add(Not(And(
        dis >= join_lower_int,
        dis <= join_upper_int
    )))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_exc_def_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c >= 0)


    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x, "x")

    result_lower, result_upper = interval_join([x_lower_bit_range, x_upper_bit_range], [BitVecVal(0, BIT_VECTOR_LENGTH), numbits(c)])
    result_lower_int = get_int_bound_from_bits(result_lower)
    result_upper_int = get_int_bound_from_bits(result_upper)

    dis = BV2Int(x | c, True)
    s.add(
        Not(And(
        dis >= result_lower_int,
        dis <= result_upper_int
    )))

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_exc_def_neg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c < 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    bound = Max(numbits(c), Max(Abs(x_lower_bit_range), Abs(x_upper_bit_range)))
    lower = get_int_bound_from_bits(-bound)
    upper = get_int_bound_from_bits(bound)

    s.add(Abs(BV2Int(x_lower_bit_range)) <= BIT_VECTOR_LENGTH - 1,
          x_upper_bit_range <= BIT_VECTOR_LENGTH - 1)

    dis = BV2Int(x | c, True)
    s.add(Not(And(
        dis >= lower,
        dis <= upper
    )))

    assert s.check() == unsat, f'Counterexample: {s.model()}'