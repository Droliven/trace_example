#!/usr/bin/env python
# encoding: utf-8
'''
@project : trace_example
@file    : recurse.py
@author  : Droliven
@contact : droliven@163.com
@ide     : PyCharm
@time    : 2021-05-07 11:35
'''

def recurse(level):
    print('recurse({})'.format(level))
    if level:
        recurse(level - 1)

def not_called():
    print('This function is never called.')
