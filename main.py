import math
import re
import matplotlib.pyplot as plt
import numpy as np

LINE = "-----------------------------------------"
def frm(num): return "{:.4f}".format(num)
def print_err(): print("Incorrect command. To see the list of commands, type \"h\".")


def get_func_description(id, coef):
    if      id == 0:    return "y' = sin(x + (" + coef + ")) / y^2"
    elif    id == 1:    return "y' = x^2 - (" + coef + ") * y"
    else:               return "y' = 0.00001 * (" + coef + ") * xy"


def ret_functions(inp):
    id, coef = int(inp.split()[1]), float(inp.split()[2])

    if id == 0:
        func        = lambda x, y:    math.sin(x + coef) / y**2
        solution    = lambda x, c:    np.cbrt(-3 * math.cos(x + coef) + c)
        calc_c      = lambda x, y:    y**3 + 3 * math.cos(x + coef)
    elif id == 1:
        func        = lambda x, y:    x**2 - coef*y
        solution    = lambda x, c:    x**2/coef - 2*(coef*x - 1)/coef**3 + c/(math.e**(coef*x))
        calc_c      = lambda x, y:    (y - x**2/coef + 2*(coef*x - 1)/coef**3) * math.e**(coef*x)
    else:
        func        = lambda x, y:    0.00001*coef*x*y
        solution    = lambda x, c:    math.e**(0.00001*coef*x**2/2 + c)
        calc_c      = lambda x, y:    math.log(y) - 0.00001*coef*x**2/2
    
    print("The entered function is: \n" + get_func_description(id, frm(coef)))
    return func, solution, calc_c


def print_help():
    print(  LINE + "\n"
            "Command list:\n\n"
            "eq [id] [coef] -- choose a differential equation:")

    for i in range(3):
        print("     " + str(i) + ": " + get_func_description(i, "[coef]"))
        
    print(  "p [x0] [x1] [y] [n] -- set the parameters for solving;\n\n"
            "calc -- calculate;\n\n"
            "h -- display this message;\n"
            "q -- quit\n" +
            LINE)


def split_args(inp):
    x0, x1, y0, n = \
        float(inp.split()[1]), float(inp.split()[2]), float(inp.split()[3]), int(inp.split()[4])
    print("x0 = " + frm(x0) + "; x1 = " + frm(x1) + "; y0 = " + frm(y0) + "; n = " + str(n) + ".")
    return x0, x1, y0, n


def plot_solution(x0, x1, solution, c):
    x = np.linspace(x0, x1, 1000)
    y = np.array([solution(xi, c) for xi in x])
    plt.plot(x, y, 'k:', label="Analytic solution")


def plot_points(points):
    x, y = np.array(points[0]), np.array(points[1])
    plt.plot(x, y, 'g', label="Euler method")


def plot_show():
    plt.title("Differential equation solution")
    plt.legend(loc='upper left')
    plt.show()


def method(x0, x1, y0, n, func):
    xarr, yarr, y, x, step = [], [], y0, x0, (x1-x0)/n
    for _ in range(n):
        x       += step
        y       += step * func(x, y)
        xarr    += [x]
        yarr    += [y]

    return (xarr, yarr)


def calc(x0, x1, y0, n, func, solution, calc_c):
    try:
        plot_points(method(x0, x1, y0, n, func))
        plot_solution(x0, x1, solution, calc_c(x0, y0))
        plot_show()
    except ZeroDivisionError:
        print(  "Encountered a division by zero while trying to calculate the solution.\n"
                "Please use different arguments.")
    except OverflowError:
        print(  "Encountered an overflow error while trying to calculate the solution.\n"
                "Please use different arguments.")
    

def prompt():
    x0, x1, y0, n = -10, 10, 1, 1000
    func, solution, calc_c = lambda x, y: 0, lambda x, c: c, lambda x, y: y
    while True:
        try:                inp = input("> ")
        except EOFError:    break

        if re.match(r"^eq [0-2] -?\d+.?\d*$", inp):
            func, solution, calc_c = ret_functions(inp)
        elif re.match(r"^p -?\d+.?\d* -?\d+.?\d* -?\d+.?\d* \d+$", inp):
            x0, x1, y0, n = split_args(inp)
        
        elif inp == "calc": calc(x0, x1, y0, n, func, solution, calc_c)
        elif inp == "h":    print_help()
        elif inp == "q":    break
        else:               print_err()


print(  "Welcome to the differential equation calculator.\n" 
        "To see the list of commands, type \"h\". To quit, type \"q\".\n" + LINE)
prompt()