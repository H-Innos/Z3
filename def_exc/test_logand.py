from z3 import Solver, BitVec, BitVecVal, BV2Int, And, unsat, Not, Abs
from helpers import Min, Max, interval_join, numbits
from constants import BIT_VECTOR_LENGTH
from def_exc.utils import initialize_bit_interval, get_int_bound_from_bits, get_unsinged_int_bound_from_bits


def test_logand_exc_exc():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    y = BitVec("y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")

    join_lower, join_upper = interval_join([x_lower_bit_range, x_upper_bit_range],[y_lower_bit_range, y_upper_bit_range])

    join_lower_int = get_int_bound_from_bits(join_lower)
    join_upper_int = get_int_bound_from_bits(join_upper)

    con = BV2Int(x & y, True)

    s.add(Not(And(con <= join_upper_int, con >= join_lower_int)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_exc_either_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    y = BitVec("y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")
    s.add(x_lower_bit_range >= 0)

    lower = BitVecVal(0, BIT_VECTOR_LENGTH)

    upper = x_upper_bit_range

    lower_int = get_int_bound_from_bits(lower)
    upper_int = get_int_bound_from_bits(upper)

    con = BV2Int(x & y, True)

    s.add(
        Not(And(con <= upper_int, con >= lower_int))
    )
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_nneg_exc_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    y = BitVec("y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x, "x")
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")
    s.add(x_lower_bit_range >= 0, y_lower_bit_range >= 0)

    lower = BitVecVal(0, BIT_VECTOR_LENGTH)

    upper = Min(x_upper_bit_range, y_upper_bit_range)

    lower_int = get_int_bound_from_bits(lower)
    upper_int = get_int_bound_from_bits(upper)

    con = BV2Int(x & y, True)

    s.add(
        Not(And(con <= upper_int, con >= lower_int))
    )
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_nneg_def_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c >= 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    s.add(x_lower_bit_range == 0, x_upper_bit_range > 0)

    result_lower, result_upper = BitVecVal(0, BIT_VECTOR_LENGTH), Min(x_upper_bit_range, numbits(c))
    result_lower_int = get_int_bound_from_bits(result_lower)
    result_upper_int = get_int_bound_from_bits(result_upper)

    con = BV2Int(x & c, True)

    s.add(Not(And(con <= result_upper_int, con >= result_lower_int)))

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_def_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c >= 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    result_lower, result_upper = interval_join([x_lower_bit_range, x_upper_bit_range], [0, numbits(c)])
    result_lower_int = get_unsinged_int_bound_from_bits(result_lower)
    result_upper_int = get_unsinged_int_bound_from_bits(result_upper)

    con = BV2Int(x & c, True)

    s.add(Not(And(con <= result_upper_int, con >= result_lower_int)))

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_nneg_def_neg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c < 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    s.add(x_lower_bit_range == 0, x_upper_bit_range > 0)

    result_lower, result_upper = BitVecVal(0, BIT_VECTOR_LENGTH), Max(numbits(c), Max(x_lower_bit_range, x_upper_bit_range))
    result_lower_int = get_unsinged_int_bound_from_bits(result_lower)
    result_upper_int = get_unsinged_int_bound_from_bits(result_upper)

    con = BV2Int(x & c, True)

    s.add(Not(And(con <= result_upper_int, con >= result_lower_int)))

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_exc_def_neg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c < 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)

    bound = Max(numbits(c), Max(Abs(x_lower_bit_range), Abs(x_upper_bit_range)))
    lower = get_int_bound_from_bits(-bound)
    upper = get_int_bound_from_bits(bound)

    s.add(Abs(BV2Int(x_lower_bit_range)) <= BIT_VECTOR_LENGTH-1,
          x_upper_bit_range <= BIT_VECTOR_LENGTH-1)

    con = BV2Int(x & c, True)
    s.add(Not(And(
        con >= lower,
        con <= upper
    )))

    assert s.check() == unsat, f'Counterexample: {s.model()}'