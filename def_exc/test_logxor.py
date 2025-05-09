from z3 import Solver, BitVecs, BitVec, BV2Int, unsat, Not, Abs, And, BitVecVal

from constants import BIT_VECTOR_LENGTH
from def_exc.utils import initialize_bit_interval, get_int_bound_from_bits
from helpers import Max, numbits


def test_logxor_exc_exc():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x, "x")
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")

    bound =  Max(Max(Abs(x_lower_bit_range), x_upper_bit_range), Max(Abs(y_lower_bit_range), y_upper_bit_range))
    lower = -bound
    upper = bound

    lower_int = get_int_bound_from_bits(lower)
    upper_int = get_int_bound_from_bits(upper)

    xor = BV2Int(x ^ y, True)
    s.add(Not(And(
        xor >= lower_int,
        xor <= upper_int
    )))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logxor_exc_nneg_exc_nneg():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x, "x")
    y_lower_bit_range, y_upper_bit_range, y_lower_int_range, y_upper_int_range = initialize_bit_interval(s, y, "y")
    s.add(x_lower_bit_range >= 0, y_lower_bit_range >= 0)

    lower = BitVecVal(0, BIT_VECTOR_LENGTH)
    upper = Max(x_upper_bit_range, y_upper_bit_range)

    lower_int = get_int_bound_from_bits(lower)
    upper_int = get_int_bound_from_bits(upper)

    xor = BV2Int(x ^ y, True)
    s.add(Not(And(
        xor >= lower_int,
        xor <= upper_int
    )))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logxor_exc_nneg_def_nneg():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    c = BitVec("c", BIT_VECTOR_LENGTH)
    s.add(c >= 0)

    x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range = initialize_bit_interval(s, x)
    s.add(x_lower_bit_range >= 0)

    bound = Max(numbits(c), Abs(x_upper_bit_range))
    lower = BitVecVal(0, BIT_VECTOR_LENGTH)
    upper = bound

    lower_int = get_int_bound_from_bits(lower)
    upper_int = get_int_bound_from_bits(upper)

    s.add(Abs(BV2Int(x_lower_bit_range)) <= BIT_VECTOR_LENGTH,
          x_upper_bit_range <= BIT_VECTOR_LENGTH)

    xor = BV2Int(x ^ c, True)
    s.add(Not(And(
        xor >= lower_int,
        xor <= upper_int
    )))

    assert s.check() == unsat, f'Counterexample: {s.model()}'