from z3 import Solver, BitVec, BitVecs, BV2Int, unsat, Not, And, Abs, BitVecVal

from constants import BIT_VECTOR_LENGTH
from def_exc.utils import initialize_bit_interval, get_int_bound_from_bits, numbits
from helpers import Max
from interval_ops import interval_join


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
    assert s.check() == unsat, (f'Counterexample:´\n x bitrange: [{s.model().eval(BV2Int(x_lower_bit_range, True))},'
                                f'{s.model().eval(BV2Int(x_upper_bit_range, True))}]\n'
                                f'x intrange: [{s.model().eval(x_lower_int_range)}, '
                                f'{s.model().eval(x_upper_int_range)}] \n'
                                f'x = {s.model().eval(BV2Int(x, True))} \n'
                                f'y = {s.model().eval(BV2Int(y, True))}\n'
                                f'y bitrange: [{s.model().eval(BV2Int(y_lower_bit_range, True))},'
                                f'{s.model().eval(BV2Int(y_upper_bit_range, True))}]\n'
                                f'y intrange: [{s.model().eval(y_lower_int_range)}, '
                                f'{s.model().eval(y_upper_int_range)}] \n'
                                f'result bitrange: [{s.model().eval(join_lower)}, {s.model().eval(join_upper)}]\n'
                                f'result intrange: [{s.model().eval(join_lower_int)}, {s.model().eval(join_upper_int)}]\n'
                                f'dis = {s.model().eval(dis)} \n')

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

    assert s.check() == unsat, (f'Counterexample:´\n x bitrange: [{s.model().eval(BV2Int(x_lower_bit_range, True))},'
                                f'{s.model().eval(BV2Int(x_upper_bit_range, True))}]\n'
                                f'x intrange: [{s.model().eval(x_lower_int_range)}, '
                                f'{s.model().eval(x_upper_int_range)}] \n'
                                f'x = {s.model().eval(BV2Int(x, True))} \n'
                                f'c = {s.model().eval(BV2Int(c, True))}\n'
                                f'result bitrange: [{s.model().eval(result_lower)}, {s.model().eval(result_upper)}]\n'
                                f'result intrange: [{s.model().eval(result_lower_int)}, {s.model().eval(result_upper_int)}]\n'
                                f'dis = {s.model().eval(dis)} \n')

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

    assert s.check() == unsat, (f'Counterexample:{s.model()}\nx bitrange: [{s.model().eval(BV2Int(x_lower_bit_range))},'
                                f'{s.model().eval(BV2Int(x_upper_bit_range))}]\n'
                                f'x intrange: [{s.model().eval(x_lower_int_range)}, '
                                f'{s.model().eval(x_upper_int_range)}] \n'
                                f'x = {s.model().eval(BV2Int(x, True))} \n'
                                f'c = {s.model().eval(BV2Int(c, True))}\n'
                                f'result bitrange: [{s.model().eval(-bound)}, {s.model().eval(bound)}]\n'
                                f'result intrange: [{s.model().eval(lower)}, {s.model().eval(upper)}]\n'
                                f'dis = {s.model().eval(dis)} \n'
                                f'numbits = {s.model().eval(numbits(c))} \n')