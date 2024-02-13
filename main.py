# Created by Zaytsev Artem s367221
# 6 variant
import cli
import slae_solver
from cli import Question, Respond, BACK_OPTION
from matrix import Matrix
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
    error_exit(NOT_SQUARE)

if a.get_determinant() == 0:
    error_exit(ZERO_DETERMINANT)

if not a.is_diagonal_dominance():
    new_matrix, new_b = a.reduce_diagonal_dominance(b)

    a = Matrix.from_list(new_matrix)
    b = new_b.copy()

    if not a.is_diagonal_dominance():
        print(NO_DIAGONAL_DOMINANCE)

# --- CHECK ---

# Now let's solve our SoLAE (System of linear algebraic equations)

slae_solver.simple_iteration(a, b, epsilon)
