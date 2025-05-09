from z3 import BitVecVal

# Some tests take a very long time to run on 32-bit numbers, can be set to 32 when running specific tests (UINT_MAX and INT_MAX also need to be updated)
BIT_VECTOR_LENGTH = 16 #32
ONE = BitVecVal(0x1, BIT_VECTOR_LENGTH)
ZERO = BitVecVal(0x0, BIT_VECTOR_LENGTH)
UINT_MAX = BitVecVal(65535, BIT_VECTOR_LENGTH) #4294967295
INT_MAX = BitVecVal(32768, BIT_VECTOR_LENGTH) # 2147483647