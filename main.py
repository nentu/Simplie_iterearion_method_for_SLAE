# Created by Zaytsev Artem s367221
# 6 variant
import cli
import slae_solver
from cli import Question, Respond, BACK_OPTION
from matrix import Matrix, get_potential_places
from my_constants import *
from utils import *

a, b, epsilon_list = Matrix(), list(), list()

cli.request(
    Question(GREETING,
             [
                 Respond(ENTER_MATRIX_OPTION,
                         Question(
                             ENTER_MATRIX_TYPE_MSG,
                             [Respond(FILE_MATRIX, lambda: cli.read_matrix_file(a, b, epsilon_list)),
                              Respond(CONSOLE_MATRIX, lambda: cli.read_matrix_console(a, b, epsilon_list)),
                              Respond(RANDOM_MATRIX, lambda: cli.random_matrix(a, b, epsilon_list)),
                              BACK_OPTION]
                         )),
                 Respond(ENTER_RULE_OPTION,
                         Question(
                             ENTER_RULE,
                             [BACK_OPTION]
                         )
                         ),
                 Respond(MATRIX_COND_OPTION,
                         Question(
                             MATRIX_COND,
                             [BACK_OPTION]
                         )),
                 Respond(ABOUT_ME_OPTION,
                         Question(
                             ABOUT_ME,
                             [BACK_OPTION]
                         )),
                 Respond(EXIT,
                         exit)
             ])
)

epsilon = epsilon_list[0]

print(YOU_ENTERED)
cli.print_matrix(a, b)

# --- CHECK ---
if not a.is_square():
    error_exit(NOW_SQUARE)

if a.get_determinant() == 0:
    error_exit(ZERO_DETERMINANT)



if not a.is_diagonal_dominance():
    potential_places = get_potential_places(a)

    # empty_rows = len(a)

    paths = get_unique_sequence(potential_places)

    if paths is not None:
        new_matrix = Matrix()
        new_matrix.fill_zeroes(len(a), len(a))
        new_b = [0 for i in range(len(b))]

        for original_row, new_row in paths:
            new_matrix[new_row] = a[original_row]
            new_b[new_row] = b[original_row]

        a = Matrix.from_list(new_matrix)
        b = new_b.copy()

    # changed = True
    # while changed:
    #     changed = False
    #     for row_i in range(len(potential_places) - 1, -1, -1):
    #         if len(potential_places[row_i]) == 1:
    #             index = potential_places[row_i][0]
    #
    #             new_matrix[index] = a[row_i].copy()
    #             new_b[index] = b[row_i]
    #
    #             potential_places[row_i].clear()
    #             del_from_row(potential_places, index)
    #             empty_rows -= 1
    #             changed = True
    if not a.is_diagonal_dominance():
        print(NO_DIAGONAL_DOMINANCE)

# --- CHECK ---

# Now let's solve our SoLAE (System of linear algebraic equations)

slae_solver.solve(a, b, epsilon)
