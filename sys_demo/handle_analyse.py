#!/usr/bin/env python
# encoding: utf-8
'''
@project : trace_example
@file    : handle_analyse.py
@author  : Droliven
@contact : droliven@163.com
@ide     : PyCharm
@time    : 2021-05-07 19:37
'''

import os
import re


def filter_comments(path):
    # 过滤注释，分析有效代码
    with open(path, 'r', encoding='UTF-8') as f:
        # data_whole = f.read()
        data_lines = f.readlines()

    valid_line_info = {}
    multi_line_comment_start = ''
    for idx, line in enumerate(data_lines):
        if multi_line_comment_start != '':
            # 处于多行注释内
            if re.match("\s*" + multi_line_comment_start + '.*', line):
                multi_line_comment_start = ''  # 结束多行注释

        elif re.match("\s*'''.*", line) or re.match('\s*""".*', line):
            # 进入多行注释
            multi_line_comment_start = line[:3]

        elif re.match('\n', line) or re.match("\s*#.*", line):
            continue
        else:
            # valid code
            valid_line_info[idx + 1] = line

    return valid_line_info


valid_line_info = filter_comments(os.path.join("E://PythonWorkspace/trace_example/sys_demo/mycode.py"))
# print(re.match('\s*', "def not_called():"))
pass
