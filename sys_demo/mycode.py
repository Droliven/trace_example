#!/usr/bin/env python
# encoding: utf-8
'''
@project : trace_example
@file    : mycode.py
@author  : Droliven
@contact : droliven@163.com
@ide     : PyCharm
@time    : 2021-05-07 11:35
'''


def not_called():
    print('This function is never called.')


def add(a, b):
    c = a + b
    return c


def loop(level):
    print('recurse({})'.format(level))
    if level > 0:
        loop(level - 1)


def main_func():
    print('This is the main program.')
    if add(2, 3) == 5:
        print("Right!")
    elif add(2, 3) == 4:
        print("Wrong.")

    loop(2)

    try:
        a = 2 / 0
    except ZeroDivisionError:
        print("ZeroDivisionError: division by zero")
    else:
        print("Successfully!")


if __name__ == '__main__':
    main_func()
