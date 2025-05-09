from z3 import BV2Int, Abs, BitVecs, If, IntVal, BitVecVal, Extract
from constants import BIT_VECTOR_LENGTH, UINT_MAX, ONE, INT_MAX

# calculates the interval that corresponds to the DefExc bit interval
def get_int_bound_from_bits(bits):
    return If(BV2Int(bits, True) <= 0,
              If(BV2Int(bits, True) == 0,
                 IntVal(0),
                 If(BV2Int(bits, True) == -BIT_VECTOR_LENGTH, # had to hardcode this to avoid overflow
                    -BV2Int(UINT_MAX),
                    If(BV2Int(bits, True) == -BIT_VECTOR_LENGTH + 1, # had to hardcode this because bit shifting in Z3 sometimes behaves unexpectedly
                       IntVal(-INT_MAX - 1),
                       -BV2Int(ONE << Abs(bits), True)
                       )
                    )
                 ),
              If(BV2Int(bits, True) == BIT_VECTOR_LENGTH,
                 BV2Int(UINT_MAX),
                 BV2Int(ONE << bits) - 1, True)
              )

def get_unsinged_int_bound_from_bits(bits):
    return If(BV2Int(bits) == 0, IntVal(0),
              If(bits == BIT_VECTOR_LENGTH,
                 BV2Int(UINT_MAX),
                 BV2Int(ONE << bits) - 1)
              )

# initializes interval bounds and sets the necessary constraints in the solver
def initialize_bit_interval(s, x, name="x"):
    x_int = BV2Int(x, True)
    x_lower_bit_range, x_upper_bit_range = BitVecs(f'l{name} u{name}', BIT_VECTOR_LENGTH)

    s.add(x_lower_bit_range <= 0, x_upper_bit_range > 0) # interval must contain 0

    s.add(
        Abs(BV2Int(x_lower_bit_range, True)) <= BIT_VECTOR_LENGTH, # interval cannot be longer than bitvector length
        x_upper_bit_range <= BIT_VECTOR_LENGTH,
        x_lower_bit_range <= x_upper_bit_range # must be correct interval
        )

    # initialize corresponding int interval
    x_lower_int_range = get_int_bound_from_bits(x_lower_bit_range)
    x_upper_int_range = get_int_bound_from_bits(x_upper_bit_range)

    # x must be in interval
    s.add(x_int <= x_upper_int_range,
          x_int >= x_lower_int_range)
    return x_lower_bit_range, x_upper_bit_range, x_lower_int_range, x_upper_int_range

























