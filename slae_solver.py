from matrix import Matrix
from my_constants import *
from utils import *


def solve(matrix: Matrix, b: list, epsilon: float, max_bad_epochs=100):
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
