from file_read import get_dots, Dot
from painter import draw
from spline import cubic_spline_interpolation
from math import *

def main():
    filename = str(input('Имя файла>'))
    dots = get_dots(filename)
    func = str(input('Функция>'))
    dots_test = []
    for dot in dots:
        x = dot.x
        y = eval(func)
        dots_test.append(Dot(x=x, y=y))
    splines = cubic_spline_interpolation(dots_test)
    draw(func=func, dots=dots, splines=splines)

if __name__ == '__main__':
    main()
