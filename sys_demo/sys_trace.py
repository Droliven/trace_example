#!/usr/bin/env python
# encoding: utf-8
'''
@project : trace_example
@file    : sys_trace.py
@author  : Droliven
@contact : droliven@163.com
@ide     : PyCharm
@time    : 2021-05-07 16:38
'''
import os
import sys
from mycode import main_func
import inspect
from handle_analyse import filter_comments

class Tracer:
    def __init__(self, code_path):
        self.valid_line_info = filter_comments(code_path)
        self.call_queue = []
        self.count_info = {}
        for k in self.valid_line_info:
            self.count_info[k] = 0
        self.exec_path = []

    def dump(self, frame, event, arg):
        '''

        :param frame: 堆栈信息
        :param event: call, line, exception, return
        :param arg:
        :return:
        '''
        # print(type(frame))
        # print(frame.__dir__())
        '''
        'f_back', 'f_code', 'f_builtins', 'f_globals', 'f_lasti', 'f_trace_lines', 'f_trace_opcodes', 'f_locals', 'f_lineno', 'f_trace'
        '''
        # print(f"+++++ {frame.f_back}, "
        #       # f"{frame.f_builtins}, "
        #       f"{frame.f_globals['__name__']}, {frame.f_lasti}, "
        #       # f"{frame.f_trace_lines}, {frame.f_trace_opcodes}, "
        #       f"{frame.f_locals}, {frame.f_trace}")
        back_frame = frame.f_back
        # print(back_frame.__dir__())
        if back_frame:
            back_code = back_frame.f_code
            back_module = inspect.getmodule(back_code)
            back_module_name = ""
            back_module_path = ""
            if back_module:
                back_module_path = back_module.__file__
                if back_module_path.__contains__("/"):
                    back_module_path = back_module_path.split("/")[-1]
                elif back_module_path.__contains__("\\"):
                    back_module_path = back_module_path.split("\\")[-1]

                back_module_name = back_module.__name__

        code = frame.f_code
        module = inspect.getmodule(code)
        module_name = ""
        module_path = ""
        if module:
            module_path = module.__file__
            if module_path.__contains__("/"):
                module_path = module_path.split("/")[-1]
            elif module_path.__contains__("\\"):
                module_path = module_path.split("\\")[-1]
            module_name = module.__name__
        if back_frame:
            print(">>> {}, ({}, {}, {}, {}), ({}, {}, {}, {}, {}, {})".format(event, back_module_path, back_module_name,
                                                                          back_frame.f_lineno, back_code.co_name,
                                                                          module_path, module_name, frame.f_lineno,
                                                                          code.co_name, frame.f_locals, arg))
        else:
            print(">>> {}, ({}, {}, {}, {}, {}, {})".format(event,
                                                        module_path, module_name, frame.f_lineno,
                                                        code.co_name, frame.f_locals, arg))

        if event == "call" or event == "line":
            # 记录代码执行路径
            self.exec_path.append({frame.f_lineno: self.valid_line_info[frame.f_lineno]})
            # 统计代码执行次数，覆盖率
            self.count_info[frame.f_lineno] = self.count_info[frame.f_lineno] + 1

        if event == "call":
            self.call_queue.append({'opt': 'C', 'module': code.co_name})
        elif event == "return":
            self.call_queue.append({'opt': 'R', 'module': back_code.co_name})

    def trace(self, frame, event, arg):
        self.dump(frame, event, arg)
        return self.trace

    def collect(self, func, *args, **kwargs):
        sys.settrace(self.trace)
        func(*args, **kwargs)
        sys.settrace(None)


if __name__ == "__main__":
    t = Tracer(os.path.join("mycode.py"))
    t.collect(main_func)

    print("\n===========================")
    print("No || Code ")
    print("---------------------------")
    for item in t.exec_path:
        for k in item:
            print_str = "{: <2d}".format(k) + " || " + item[k]
            print(print_str, end="")

    print("\n===========================")
    cnt = 0
    print("Cnt | No || Code ")
    print("---------------------------")
    for k in t.valid_line_info:
        if t.count_info[k] != 0:
            cnt += 1
        print_str = "[{: <1d}]".format(t.count_info[k]) + " | " + "{: <2d}".format(k) + " || " + t.valid_line_info[k]
        print(print_str, end="")

    print("Total lines: {}, covered lines: {}, cover rate: {:>.2f}.".format(len(t.valid_line_info), cnt, cnt / len(t.valid_line_info)))

    print("\n===========================")
    print("C/R | Module")
    print("---------------------------")
    for item in t.call_queue:
        print(" {}  | {}".format(item['opt'], item['module']))
