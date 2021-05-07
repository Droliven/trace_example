#!/usr/bin/env python
# encoding: utf-8

from recurse import recurse

def main():
    print('This is the main program.')
    if 2+3 == 5:
        print("Right!")
    elif 2+3 == 4:
        print("Wrong.")

    recurse(2)

    try:
        a = 2 / 0
    except ZeroDivisionError:
        print("ZeroDivisionError: division by zero")
    else:
        print("Successfully!")


if __name__ == "__main__":
    main()