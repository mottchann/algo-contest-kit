import sys
sys.setrecursionlimit(10**6)
from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from bisect import bisect_left, bisect_right
from math import comb, factorial, gcd, lcm, perm
from itertools import accumulate, combinations, permutations, product
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase, digits
from sortedcontainers import SortedSet, SortedList, SortedDict
MOD = 998244353
def II() -> int: return int(input())
def LI() -> list[str]: return list(input())
def LMI() -> list[int]: return list(map(int, input().split()))
def LMS() -> list[str]: return list(map(str, input().split()))
def LLMI(x: int) -> list[list[int]]: return [list(map(int, input().split())) for _ in range(x)]
def LLMS(x: int) -> list[list[str]]: return [list(input()) for _ in range(x)]


class Fenwick_Tree:
    def __init__(self, n):
        self._n = n
        self.data = [0] * n
    
    def add(self, p, x):
        assert 0 <= p < self._n
        p += 1
        while p <= self._n:
            self.data[p - 1] += x
            p += p & -p
    
    def sum(self, l, r):
        assert 0 <= l <= r <= self._n
        return self._sum(r) - self._sum(l)
    
    def _sum(self, r):
        s = 0
        while r > 0:
            s += self.data[r - 1]
            r -= r & -r
        return s


class FastFactorization():
    def __init__(self):
        self.n = 5 * 10 ** 6
        self.isprime = [0, 0] + [1] * (self.n)
        self.minfactor = [-1] * (self.n + 1)

        # Eratosthenesの篩
        for i in range(2, self.n+1):
            if self.isprime[i] == 0: continue
            self.minfactor[i] = i
            for j in range(i*2, self.n+1, i):
                self.isprime[j] = 0
                if self.minfactor[j] == -1:
                    self.minfactor[j] = i
    
    def factorize(self, n: int) -> list[tuple]:
        """
        O(logn)の高速素因数分解
        """
        res = []
        while n > 1:
            p = self.minfactor[n]
            exp = 0

            while p == self.minfactor[n]:
                n //= p
                exp += 1
            
            res.append((p, exp))
        
        return res
    
    def divisor_enumatation(self, n: int) -> list[int]:
        """
        約数列挙
        """
        res = [1]
        f = self.factorize(n)
        for p, exp in f:
            cnt = len(res)
            while exp:
                for i in range(cnt):
                    res.append(res[i] * p)
                exp -= 1
                p *= p
        
        return res

    def totient_function(self, n: int) -> int:
        """
        1以上n以下のnと互いに素な整数の個数を返す
        """
        f = self.factorize(n)
        for p, exp in f:
            n = n - n // p
        return n


def LIS(arr: list):
    """
    Longest Increasing Subsequence（最長増加部分列） 
    元の数列から順序を変えずに（連続でなくてもよい）取り出した部分列の中で、狭義単調増加しているものの最大長を返す
    """
    INF = float('INF')
    dp = [INF] * len(arr)
    for a in arr:
        idx = bisect_left(dp, a)
        dp[idx] = a
    
    res = len([i for i in dp if i != INF])
    return res


def DFS_grid(grid: list[str], s: tuple[int], g: tuple[int]) -> None:
    sx, sy = s
    gx, gy = g
    h = len(grid)
    w = len(grid[0])
    TF = [[False] * w for _ in range(h)]
    d = deque([s])

    while d:
        x, y = d.pop()
        if x == gx and y == gy:
            print('Yes')
            return
        if TF[x][y]: continue
        TF[x][y] = True
        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= x + i < h and 0 <= y + j < w:
                if grid[x+i][y+j] == '#': continue
                if TF[x+i][y+j]: continue
                d.append((x+i, y+j))
    
    print('No')
    return


def dijkstra(graph: list[list[int]], s: int) -> list[int]:
    res = [-1] * len(graph)
    heap = []
    heappush(heap, (0, s))
    while heap:
        cur_v, cur = heappop(heap)
        if res[cur] != -1: continue
        res[cur] = cur_v
        for nxt, nxt_v in graph[cur]:
            if res[nxt] != -1: continue
            heappush(heap, (cur_v + nxt_v, nxt))
    return res

def segfunc_sum(x, y):
    return x + y
def segfunc_min(x, y):
    return min(x, y)
def segfunc_max(x, y):
    return max(x, y)
def segfunc_gcd(x, y):
    return gcd(x, y)
def segfunc_lcm(x, y):
    return x // gcd(x, y) * y if x and y else 0
def segfunc_or(x, y):
    return x | y
def segfunc_and(x, y):
    return x & y
def segfunc_xor(x, y):
    return x ^ y

ide_ele_sum = 0
ide_ele_min = float('inf')
ide_ele_max = 0
ide_ele_gcd = 0
ide_ele_lcm = 1
ide_ele_or = 0
ide_ele_and = (1 << 60) - 1
ide_ele_xor = 0

class SegTree:
    """
    init(init_val, ide_ele): 配列init_valで初期化 O(N)
    update(k, x): k番目の値をxに更新 O(logN)
    query(l, r): 区間[l, r)をsegfuncしたものを返す O(logN)
    """
    def __init__(self, init_val, segfunc, ide_ele):
        """
        init_val: 配列の初期値
        segfunc: 区間にしたい操作
        ide_ele: 単位元
        n: 要素数
        num: n以上の最小の2のべき乗
        tree: セグメント木(1-index)
        """
        n = len(init_val)
        self.segfunc = segfunc
        self.ide_ele = ide_ele
        self.num = 1 << (n - 1).bit_length()
        self.tree = [ide_ele] * 2 * self.num
        # 配列の値を葉にセット
        for i in range(n):
            self.tree[self.num + i] = init_val[i]
        # 構築していく
        for i in range(self.num - 1, 0, -1):
            self.tree[i] = self.segfunc(self.tree[2 * i], self.tree[2 * i + 1])
    
    def update(self, k, x):
        """
        k番目の値をxに更新
        k: index(0-index)
        x: update value
        """
        k += self.num
        self.tree[k] = x
        while k > 1:
            self.tree[k >> 1] = self.segfunc(self.tree[k], self.tree[k ^ 1])
            k >>= 1

    def query(self, l, r):
        """
        [l, r)のsegfuncしたものを得る
        l: index(0-index)
        r: index(0-index)
        """
        res = self.ide_ele

        l += self.num
        r += self.num
        while l < r:
            if l & 1:
                res = self.segfunc(res, self.tree[l])
                l += 1
            if r & 1:
                res = self.segfunc(res, self.tree[r - 1])
            l >>= 1
            r >>= 1
        return res


def execute() -> None:
    pass


if __name__ == "__main__":
    T = 1
    for _ in range(T):
        execute()
