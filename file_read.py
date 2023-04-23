from typing import NamedTuple

class Dot(NamedTuple):
    x: float
    y: float

def get_dots(filename: str) -> list[Dot]:
    matrix = read_table(filename)
    return convert_matrix_to_dots(matrix)

def read_table(filename: str) -> list[list[float]]:
    '''Возвращает список значений функции в виде матрицы'''
    with open(filename) as file:
        matrix = [list(map(float, row.split())) for row in file.readlines()]

    return matrix 

def convert_matrix_to_dots(matrix: list[list[float]]) -> list[Dot]:
    '''Преобразует 2D матрицу значений фукнции в массив объектов Dot.
    Первая строка: значения x, втора: значения f(x)'''
    dots = []
    for i in range(len(matrix[0])):
        dots.append(Dot(x=matrix[0][i],
                        y=matrix[1][i]))
    return dots

