import cli
from matrix import Matrix
from my_constants import *
from utils import *


def gauss(matrix: Matrix, b: list):
    a = matrix
    n = len(a)
    
    x = [0 for _ in range(n)]
    for i in range(n - 1):
        k = a[i][i]
        if k == 0:
            for j in range(i + 1, n):
                if a[j][i] != 0:
                    k = a[j][i]
                    swap(a, i, j)
                    swap(b, i, j)
                    break
            else:
                return 0
        for j in range(i + 1, n):
            t = mul_vec(a[i], - a[j][i] / k)
            a[j] = sum_vec(a[j], t)

            b[j] -= b[j] * a[j][i] / k

    for i in range(n - 1, -1, -1):
        t = b[i] - sum([a[i][j] * x[j] for j in range(i + 1, n - 1)])
        x[i] = 1 / a[i][i] * t

    cli.print_matrix(a, b)


def simple_iteration(matrix: Matrix, b: list, epsilon: float, max_bad_epochs=100):
    x = b.copy()
    prev_x = [b[i] / matrix[i][i] for i in range(len(b))]

    epoch = 0
    metric = epsilon * 2

    prev_metric = metric + 1
    count_bad_metric = 0
    while metric >= epsilon:
        epoch += 1
        for i in range(len(x)):
            x[i] = b[i] / matrix[i][i] - sum(
                [matrix[i][j] / matrix[i][i] * prev_x[j] for j in range(len(prev_x)) if i != j])
        metric = mae(prev_x, x)
        prev_x = x.copy()

        if metric < prev_metric:
            count_bad_metric = 0
        else:
            count_bad_metric += 1
            if count_bad_metric > max_bad_epochs:
                error_exit(get_solae_error(max_bad_epochs))

        prev_metric = metric

        # print(EPOCHS + ':', epoch)
        # print(ERROR + ':', metric)

    print(RESULT, end=': ')
    for i in range(len(x)):
        print(f'x_{i + 1}=' + str(x[i]), end=', ' if i != len(x) - 1 else '\n')
    print(EPOCHS + ':', epoch)
    print(ERROR + ':', metric)
    print(B_MAE + ':', residual(matrix, x, b))
