from z3 import Int, solve, BitVec, BitVecs, BV2Int, If, Not
import time

def solve_logand(len:int):
    print(f'Length: {len}')
    x, y = BitVecs("x y", len)
    start = time.time()
    x_int, y_int = BV2Int(x), BV2Int(y)

    solve(Not(BV2Int(x & y) <= If(x_int > y_int, x_int, y_int)))
    end = time.time()
    print(f'Elapsed time: {end - start} s')

def solve_problem():
    for i in range(8, 32):
        solve_logand(i);

if __name__ == '__main__':
    solve_problem()