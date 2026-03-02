from collections import Counter, defaultdict, deque
from heapq import heappop, heappush
from bisect import bisect_left, bisect_right
from math import comb, factorial, gcd, lcm, perm
from itertools import accumulate, combinations, permutations, product
from functools import lru_cache
import operator
from string import ascii_lowercase, ascii_uppercase, digits

MOD = 998244353


def II() -> int:
    return int(input())


def LI() -> list[str]:
    return list(input())


def LMI() -> list[int]:
    return list(map(int, input().split()))


def LMS() -> list[str]:
    return list(map(str, input().split()))


def LLMI(x: int) -> list[list[int]]:
    return [list(map(int, input().split())) for _ in range(x)]


def LLMS(x: int) -> list[list[str]]:
    return [list(input()) for _ in range(x)]


def execute() -> None:
    pass


if __name__ == "__main__":
    T = 1
    for _ in range(T):
        execute()
