from z3 import BitVecs, Ints, BV2Int, Not, unsat, Solver, Int, BitVecVal, And

from constants import BIT_VECTOR_LENGTH
from helpers import Max, Min, min_val_bit_constrained, next_power_of_2


def test_logand_unsigned():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    ux, uy = Ints("ux uy")
    x_int, y_int = BV2Int(x), BV2Int(y)

    s.add(x_int <= ux, y_int <= uy, Not(BV2Int(x & y) <= Min(ux, uy)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_signed_both_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    ux, uy = Ints("ux uy")
    x_int, y_int = BV2Int(x, True), BV2Int(y, True)

    con = BV2Int(x & y, True)

    s.add(0 <= x_int, x_int <= ux, 0 <= y_int, y_int <= uy, Not(And(con <= Min(ux, uy), con >= 0)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_signed_both_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    ux, uy = Ints("ux uy")
    lx, ly = Ints("lx ly")
    x_int, y_int = BV2Int(x, True), BV2Int(y, True)
    con = BV2Int(x & y, True)
    s.add(ux < 0, uy < 0,
          x_int >= lx,
          x_int <= ux,
          y_int >= lx,
          y_int <= uy,
          Not(
              And(con <= 0,
              con >= min_val_bit_constrained(Min(lx, ly))
                  ))
          )
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logand_signed_positive_and_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ux, ly, uy = Ints("lx ux ly uy")

    x_int, y_int = BV2Int(x, True), BV2Int(y, True)
    con = BV2Int(x & y, True)

    s.add(lx <= x_int, x_int <= ux,
          ly <= y_int, y_int <= uy,
          ux < 0, ly >= 0,
          Not(And(con >= 0,
          con <= BV2Int(next_power_of_2(Max(x, y)))))
          )

    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_unsigned():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ly = Ints("lx ly")
    x_int, y_int = BV2Int(x), BV2Int(y)

    s.add(x_int >= lx,
          y_int >= ly,
          Not(BV2Int(x | y) >= Max(lx, ly)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_signed_both_non_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    lx, ly = Ints("lx ly")
    x_int, y_int = BV2Int(x, True), BV2Int(y, True)

    s.add(lx >= 0, ly >= 0, x_int >= lx, y_int >= ly, Not(BV2Int(x | y, True) >= Max(lx, ly)))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

def test_logor_signed_one_negative():
    s = Solver()
    x, y = BitVecs("x y", BIT_VECTOR_LENGTH)
    ux = Int("ux")
    x_int = BV2Int(x, True)

    s.add(ux < 0, x_int <= ux, Not(BV2Int(x | y, True) < 0))
    assert s.check() == unsat, f'Counterexample: {s.model()}'

