from math import sqrt

from utils import *


class Matrix(list):

    def __init__(self):
        super().__init__()

    def fill_zeroes(self, m: int, n: int):
        super().clear()
        for i in range(m):
            super().append([0 for i in range(n)])

    @staticmethod
    def from_list(origin: list):
        res = Matrix()
        res.fill_zeroes(len(origin), len(origin))
        for i in range(len(res)):
            res[i] = origin[i].copy()
        return res

    def is_square(self) -> bool:
        width = -1
        for s in self:
            if width == -1:
                width = len(s)
            if len(s) != width:
                return False
        return len(self) == width

    def get_norm(self) -> float:
        res = 0
        for i in self:
            for j in i:
                res += j ** 2
        return sqrt(res)

    def get_determinant(self) -> float:
        # self.is_square()
        res = 1
        a = self.copy()
        for i in range(len(a) - 1):
            k = a[i][i]
            if k == 0:
                for j in range(i + 1, len(a)):
                    if a[j][i] != 0:
                        k = a[j][i]
                        swap(a, i, j)
                        res *= -1
                        break
                else:
                    return 0
            res *= k
            for j in range(i + 1, len(a)):
                t = mul_vec(a[i], - a[j][i] / k)
                a[j] = sum_vec(a[j], t)
        res *= a[-1][-1]
        return res

    # def get_determinant(self):
    #     if not self.is_square():
    #         return -1
    #
    #     for i in self:
    #         if len(i) != len(self) or len(i) != len(self[0]):
    #             return -1
    #     perms = list(permutations(range(len(self))))
    #
    #     res = 0
    #     for perm in perms:
    #         t = 1
    #         for j in range(len(self)):
    #             t *= self[j][perm[j]]
    #         if not parity_permutation(perm):
    #             t *= -1
    #         res += t
    #     return res

    def is_diagonal_dominance(self) -> bool:
        res = False
        for i in range(len(self)):
            summ = sum(abs(self[i][j]) for j in range(len(self)) if i != j)
            if not self[i][i] >= summ:
                return False
            if self[i][i] > summ:
                res = True
        return res

    def _max_column_index(self, column: int) -> int:
        return max(enumerate(self), key=lambda x: x[1][column])[0]

    def swap(self, i: int, j: int):
        swap(self, i, j)


if __name__ == '__main__':
    a = Matrix()
    for i in range(1, 14, 4):
        a.append([j ** 2 for j in list(range(i, i + 4))])
    print(a)
    print(a.get_determinant())
