from z3 import BitVec, BV2Int, Ints, Solver, solve, Not, And, Abs, Int, BitVecs, unsat

from constants import BIT_VECTOR_LENGTH
from helpers import Max, Min, get_int_bound_from_bits

def test_logand_exc_exc():
    s = Solver()
    x = BitVec("x", BIT_VECTOR_LENGTH)
    y = BitVec("y", BIT_VECTOR_LENGTH)

    x_int, y_int = BV2Int(x), BV2Int(y)

    x_lower_bit_range, x_upper_bit_range, y_lower_bit_range, y_upper_bit_range = BitVecs("lx ux ly uy",
                                                                                         BIT_VECTOR_LENGTH)
    x_lower_int_range = get_int_bound_from_bits(x_lower_bit_range)
    x_upper_int_range = get_int_bound_from_bits(x_upper_bit_range)
    y_lower_int_range = get_int_bound_from_bits(y_lower_bit_range)
    y_upper_int_range = get_int_bound_from_bits(y_upper_bit_range)

    meet_lower = Max(x_lower_bit_range, y_lower_bit_range)
    meet_upper = Min(x_upper_bit_range, y_upper_bit_range)

    meet_int_lower = 0
    meet_int_upper = get_int_bound_from_bits(meet_upper)

    con = BV2Int(x & y)

    s.add(Abs(x_lower_bit_range) <= BIT_VECTOR_LENGTH,
        x_lower_bit_range <= x_upper_bit_range,
        x_upper_bit_range <= BIT_VECTOR_LENGTH,
        Abs(y_lower_bit_range) <= BIT_VECTOR_LENGTH,
        y_lower_bit_range <= y_upper_bit_range,
        y_upper_bit_range <= BIT_VECTOR_LENGTH,
        x_int <= x_upper_int_range,
          x_int >= x_lower_int_range,
          y_int <= y_upper_int_range,
          y_int >= y_lower_int_range,
          Not(And(con <= meet_int_upper, con >= meet_int_lower))
          )
    assert s.check() == unsat, f'Counterexample:{s.model()} {s.model().eval(con)}'