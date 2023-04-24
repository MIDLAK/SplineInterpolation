from file_read import get_dots, Dot
from painter import draw
from spline import cubic_spline_interpolation
from math import *
import printer

def main():
    # выбор режима работы
    printer.print_working_mode_message() 
    working_mode = str(input('>'))

    # получение узлов интерполяции из файла
    filename = str(input('Имя файла>'))
    dots = get_dots(filename=filename)

    match working_mode:
        case '1': # по таблице
            splines = cubic_spline_interpolation(dots=dots)
            user_x = float(input('x>'))
            for i in range(len(dots)-1):
                if user_x >= dots[i].x and user_x <= dots[i+1].x:
                    spl = splines[i]
                    spl_value = spl.a + spl.b*(user_x-spl.x) + \
                            spl.c/2*((user_x-spl.x)**2) + \
                            spl.d/6*((user_x-spl.x)**3)
                    print(f'S({user_x}) = {spl_value}')

        case '2': # по функции
            func = str(input('Функция>'))
            dots_func = []
            for dot in dots:
                x = dot.x
                y = eval(func)
                dots_func.append(Dot(x=x, y=y))
            splines = cubic_spline_interpolation(dots_func)
            draw(func=func, dots=dots, splines=splines)

if __name__ == '__main__':
    main()
