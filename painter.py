import matplotlib.pyplot as plt
import numpy as np
from math import *
from file_read import Dot
from spline import SplineFunction
from dataclasses import dataclass

STEP_X = 0.001
DOT_COLOR = '#c9007a'

@dataclass
class Interval:
    left: float
    right: float

def draw(func: str, dots: list[Dot], splines: list[SplineFunction] | None) -> None:
    '''Отрисовка переданной фукнции func на интервале
    расположения точек dots. Дополнительно можно передать сплайны'''
    # настройка поля для рисования
    plt.ylabel('y')
    plt.xlabel('x')
    plt.grid(True)

    # получение интервала и его разбиение с шагом STEP_X
    interval = get_interval(dots)
    x_range = list(np.arange(interval.left, interval.right, STEP_X))

    # построение функции и отрисовка
    func_values = function_calculate(func, x_range)

    # вычисление сплайнов
    if splines != None:
        spline_values = []
        for x in x_range:
            for i in range(len(dots)-1):
                if x >= dots[i].x and x <= dots[i+1].x:
                    spl = splines[i]
                    spline_values.append(spl.a + spl.b*(x-spl.x) + \
                            spl.c/2*((x-spl.x)**2) + spl.d/6*((x-spl.x)**3))
        plt.plot(x_range, spline_values, label=f'S(x) for {func}')

    # отрисовка истинной фукнции и точек
    plt.plot(x_range, func_values, label=func)
    for dot in dots:
        x = dot.x
        plt.scatter(x, eval(func), color=DOT_COLOR)
    plt.legend()
    plt.show()

def get_interval(dots: list[Dot]) -> Interval:
    '''Возвращает границы интервала расположения точек dots'''
    left = dots[0].x
    right = dots[0].x
    for dot in dots:
        x = dot.x
        if x < left:
            left = x
        if x > right:
            right = x
    return Interval(left=left, right=right)

def function_calculate(func: str, x_values: list[float]) -> list[float]:
    '''Вычисляет для значений x_values значения фукнции func'''
    func_values = []
    for x in x_values:
        func_values.append(eval(func))
    return func_values

