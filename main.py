from z3 import Solver, BitVecVal

import logand
import test
from constants import BIT_VECTOR_LENGTH
from helpers import get_int_bound_from_bits


def main():
    s = Solver()

    s.check()

    print(f'{s.model().eval(get_int_bound_from_bits(BitVecVal(-7, BIT_VECTOR_LENGTH)))}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

