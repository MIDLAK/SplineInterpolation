from file_read import Dot
from typing import NamedTuple

class SplineFunction(NamedTuple):
    '''S[i] = a + b*(x-x[i]) + c/2*(x-x[i])**2 + d/6*(x-x[i])**3'''
    a: float = 0.0
    b: float = 0.0
    c: float = 0.0 # для первого уравнения так и останется
    d: float = 0.0
    x: float = 0.0

def cubic_spline_interpolation(dots: list[Dot]) -> list[SplineFunction]:
    # вычисление шага
    h = get_steps(dots) 

    # вычисление свободных коэффициентов для матрицы c
    free_coefficients = []
    for i in range(len(dots)-2):
        free_coefficients.append(6*((dots[i+2].y - dots[i+1].y)/h[i+1] - \
                                   (dots[i+1].y - dots[i].y)/h[i]))

    # вычисление матрицы C
    c_matrix = []
    for i in range(len(dots)-2):
        c_matrix.append([0]*(len(dots)-2)) 
        for j in range(len(dots)-2):
            if i == j:
                c_matrix[i][j] = 2*(h[i]+h[i+1])
            elif j == i + 1:
                c_matrix[i][j] = h[i+1]
            elif j == i - 1:
                c_matrix[i][j] = h[i]
            else:
                c_matrix[i][j] = 0.0

    # вычисление всех неизвестных c методом прогонки
    c = sweep_method(c_matrix, free_coefficients)
    # c_0 и c_n равны нулю
    c.append(0.0)
    c.insert(0, 0.0)


    splines = []
    # вычисление остальных коэффициентов
    for i in range(1, len(dots)):
        spline = SplineFunction(
                a=dots[i].y,
                x=dots[i].x,
                d=(c[i]-c[i-1])/h[i-1],
                b=h[i-1]/2*c[i]-(h[i-1]**2)*(c[i]-c[i-1])/h[i-1]/6+(dots[i].y-dots[i-1].y)/h[i-1],
                c=c[i])
        splines.append(spline)
    return splines

def get_steps(dots: list[Dot]) -> list[float]:
    '''Вычисление шага'''
    steps = []
    for i in range(1, len(dots)):
        steps.append(dots[i].x - dots[i-1].x)
    return steps

def sweep_method(matrix: list[list[float]], free_coefficients: list[float]) -> list[float]:
    '''Решение СЛАУ методом прогонки'''
    dimension = len(matrix)
    matrix_copy = matrix.copy()
    free_coefficients_copy = free_coefficients.copy()

    # <<спуск>>
    for i in range(1, dimension):
        matrix_copy[i][i] = matrix_copy[i][i]- \
            matrix_copy[i][i-1]*matrix_copy[i-1][i]/matrix_copy[i-1][i-1]

        free_coefficients_copy[i] = free_coefficients_copy[i]- \
                free_coefficients_copy[i-1]*matrix_copy[i][i-1]/matrix_copy[i-1][i-1]

        matrix_copy[i][i-1] = 0.0

    # <<подъём>>
    x = [0.0]*(dimension)
    x[dimension-1] = free_coefficients_copy[dimension-1]/matrix_copy[dimension-1][dimension-1]
    for i in range(dimension-2, -1, -1):
        x[i] = 1/matrix_copy[i][i]* \
                 (free_coefficients_copy[i]-x[i+1]*matrix_copy[i][i+1])
    return x




