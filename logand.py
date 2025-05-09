import time

from z3 import *

from constants import BIT_VECTOR_LENGTH
from helpers import *

def solve_logand_exc_exc():
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

    meet_int_lower = get_int_bound_from_bits(meet_lower)
    meet_int_upper = get_int_bound_from_bits(meet_upper)

    con = BV2Int(x & y)

    solve(
        x_int <= x_upper_int_range,
          x_int >= x_lower_int_range,
          y_int <= y_upper_int_range,
          y_int >= y_lower_int_range,
          Not(And(con <= meet_int_upper, con >= meet_int_lower))
          )

def solve_problem():
    """
    for i in range(8, 32):
        print(f'Length: {i}')
        start = time.time()
        solve_logand_signed_positive_and_negative(i)
        end = time.time()
        print(f'Elapsed time: {end - start} s')
    """
    start = time.time()
    solve_logand_exc_exc()
    end = time.time()
    print(f'Elapsed time: {end - start} s')

if __name__ == '__main__':
    solve_problem()