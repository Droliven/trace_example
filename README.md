# Python Trace Examples
> 软件测试的代码覆盖率与执行路径分析。网络上比较多的是利用已经实现好的包 `coverage` 来做，或者利用 `Python` 的 `trace` 库来做， 参考 [trace — 跟踪代码执行流][1], [trace --- 跟踪Python语句执行][2], 但是可以利用 sys.settrace() 通过插桩自行实现， 参考 [python插装--sys.settrace][3]。

## Coverage

首先运行测试，当前目录生成 .covetage 文件
```
coverage run test.py
coverage run --branch test.py
```
终端输出
```
This is the main program.
Right!
recurse(2)
recurse(1)
recurse(0)
ZeroDivisionError: division by zero
```

其次运行解析
```
coverage report
```
终端输出结果
```
Name         Stmts   Miss Branch BrPart  Cover
----------------------------------------------
recurse.py       7      1      2      0    89%
test.py         15      3      6      2    67%
----------------------------------------------
TOTAL           22      4      8      2    73%
```

运行解析，当前目录生成 htmlcov/ 目录，点击 index.html 打开网页
```
coverage html
```


## trace

首先运行解析，忽略 import_lib 库
```
python -m trace --ignore-dir=D:\Anaconda --trace --timing main.py
python -m trace --ignore-dir=/mnt/hdd4T/dlw_home/anaconda3 --trace --timing main.py
```

终端输出结果
```
 --- modulename: main, funcname: <module>
0.00 main.py(3): '''
0.00 main.py(12): from recurse import recurse
 --- modulename: recurse, funcname: <module>
0.01 recurse.py(3): '''
0.01 recurse.py(12): def recurse(level):
0.01 recurse.py(17): def not_called():
0.01 main.py(14): def main():
0.01 main.py(30): if __name__ == '__main__':
0.01 main.py(31):     main()
 --- modulename: main, funcname: main
0.01 main.py(15):     print('This is the main program.')
This is the main program.
0.01 main.py(16):     if 2+3 == 5:
0.01 main.py(17):         print("Right!")
Right!
0.01 main.py(21):     recurse(2)
 --- modulename: recurse, funcname: recurse
0.01 recurse.py(13):     print('recurse({})'.format(level))
recurse(2)
0.01 recurse.py(14):     if level:
0.01 recurse.py(15):         recurse(level - 1)
 --- modulename: recurse, funcname: recurse
0.01 recurse.py(13):     print('recurse({})'.format(level))
recurse(1)
0.01 recurse.py(14):     if level:
0.01 recurse.py(15):         recurse(level - 1)
 --- modulename: recurse, funcname: recurse
0.01 recurse.py(13):     print('recurse({})'.format(level))
recurse(0)
0.01 recurse.py(14):     if level:
0.01 main.py(23):     try:
0.01 main.py(24):         a = 2 / 0
0.01 main.py(25):     except ZeroDivisionError:
0.01 main.py(26):         print("ZeroDivisionError: division by zero")
ZeroDivisionError: division by zero
```

运行解析，结果保存在 ./coverdir/
```
python -m trace --ignore-dir=/mnt/hdd4T/dlw_home/anaconda3 --count --coverdir ./coverdir --file ./coverdir/coverage_report.dat main.py

```
终端输出
```
This is the main program.
Right!
recurse(2)
recurse(1)
recurse(0)
ZeroDivisionError: division by zero
```

分析代码执行覆盖率输出百分比
```
python -m trace --coverdir ./coverdir --report --summary --missing --file ./coverdir/coverage_report.dat main.py
```
输出百分比
```
lines   cov%   module   (path)
   16    81%   main   (main.py)
    7    85%   recurse   (/mnt/hdd4T/dlw_home/pythonWorkspace/trace_example/trace_demo/recurse.py)
```

分析代码的调用关系
```
python -m trace --listfuncs --trackcalls main.py | grep -v importlib
python -m trace --listfuncs --trackcalls main.py
```
终端输出
```
This is the main program.
Right!
recurse(2)
recurse(1)
recurse(0)
ZeroDivisionError: division by zero

calling relationships:

*** /mnt/hdd4T/dlw_home/anaconda3/lib/python3.8/trace.py ***
  --> main.py
    trace.Trace.runctx -> main.<module>

*** /mnt/hdd4T/dlw_home/pythonWorkspace/trace_example/trace_demo/recurse.py ***
    recurse.recurse -> recurse.recurse

  --> /mnt/hdd4T/dlw_home/pythonWorkspace/trace_example/trace_demo/recurse.py


*** main.py ***
    main.<module> -> main.main
  --> /mnt/hdd4T/dlw_home/pythonWorkspace/trace_example/trace_demo/recurse.py
    main.main -> recurse.recurse
```

## sys.settrace()

程序执行结果
```
>>> call, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 28, main_func, {}, None)
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 29, main_func, {}, None)
This is the main program.
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 30, main_func, {}, None)
>>> call, (mycode.py, mycode, 30, main_func), (mycode.py, mycode, 17, add, {'a': 2, 'b': 3}, None)
>>> line, (mycode.py, mycode, 30, main_func), (mycode.py, mycode, 18, add, {'a': 2, 'b': 3}, None)
>>> line, (mycode.py, mycode, 30, main_func), (mycode.py, mycode, 19, add, {'a': 2, 'b': 3, 'c': 5}, None)
>>> return, (mycode.py, mycode, 30, main_func), (mycode.py, mycode, 19, add, {'a': 2, 'b': 3, 'c': 5}, 5)
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 31, main_func, {}, None)
Right!
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 35, main_func, {}, None)
>>> call, (mycode.py, mycode, 35, main_func), (mycode.py, mycode, 22, loop, {'level': 2}, None)
>>> line, (mycode.py, mycode, 35, main_func), (mycode.py, mycode, 23, loop, {'level': 2}, None)
recurse(2)
>>> line, (mycode.py, mycode, 35, main_func), (mycode.py, mycode, 24, loop, {'level': 2}, None)
>>> line, (mycode.py, mycode, 35, main_func), (mycode.py, mycode, 25, loop, {'level': 2}, None)
>>> call, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 22, loop, {'level': 1}, None)
>>> line, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 23, loop, {'level': 1}, None)
recurse(1)
>>> line, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 24, loop, {'level': 1}, None)
>>> line, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 25, loop, {'level': 1}, None)
>>> call, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 22, loop, {'level': 0}, None)
>>> line, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 23, loop, {'level': 0}, None)
recurse(0)
>>> line, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 24, loop, {'level': 0}, None)
>>> return, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 24, loop, {'level': 0}, None)
>>> return, (mycode.py, mycode, 25, loop), (mycode.py, mycode, 25, loop, {'level': 1}, None)
>>> return, (mycode.py, mycode, 35, main_func), (mycode.py, mycode, 25, loop, {'level': 2}, None)
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 37, main_func, {}, None)
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 38, main_func, {}, None)
>>> exception, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 38, main_func, {}, (<class 'ZeroDivisionError'>, ZeroDivisionError('division by zero'), <traceback object at 0x000001DE1B10F580>))
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 39, main_func, {}, None)
>>> line, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 40, main_func, {}, None)
ZeroDivisionError: division by zero
>>> return, (sys_trace.py, __main__, 94, collect), (mycode.py, mycode, 40, main_func, {}, None)
```

代码执行路径分析
```
===========================
No || Code 
---------------------------
28 || def main_func():
29 ||     print('This is the main program.')
30 ||     if add(2, 3) == 5:
17 || def add(a, b):
18 ||     c = a + b
19 ||     return c
31 ||         print("Right!")
35 ||     loop(2)
22 || def loop(level):
23 ||     print('recurse({})'.format(level))
24 ||     if level > 0:
25 ||         loop(level - 1)
22 || def loop(level):
23 ||     print('recurse({})'.format(level))
24 ||     if level > 0:
25 ||         loop(level - 1)
22 || def loop(level):
23 ||     print('recurse({})'.format(level))
24 ||     if level > 0:
37 ||     try:
38 ||         a = 2 / 0
39 ||     except ZeroDivisionError:
40 ||         print("ZeroDivisionError: division by zero")
```

代码覆盖率分析
```
===========================
Cnt | No || Code 
---------------------------
[0] | 13 || def not_called():
[0] | 14 ||     print('This function is never called.')
[1] | 17 || def add(a, b):
[1] | 18 ||     c = a + b
[1] | 19 ||     return c
[3] | 22 || def loop(level):
[3] | 23 ||     print('recurse({})'.format(level))
[3] | 24 ||     if level > 0:
[2] | 25 ||         loop(level - 1)
[1] | 28 || def main_func():
[1] | 29 ||     print('This is the main program.')
[1] | 30 ||     if add(2, 3) == 5:
[1] | 31 ||         print("Right!")
[0] | 32 ||     elif add(2, 3) == 4:
[0] | 33 ||         print("Wrong.")
[1] | 35 ||     loop(2)
[1] | 37 ||     try:
[1] | 38 ||         a = 2 / 0
[1] | 39 ||     except ZeroDivisionError:
[1] | 40 ||         print("ZeroDivisionError: division by zero")
[0] | 41 ||     else:
[0] | 42 ||         print("Successfully!")
[0] | 45 || if __name__ == '__main__':
[0] | 46 ||     main_func()
Total lines: 24, covered lines: 16, cover rate: 0.67.
```

模块调用关系分析
```
===========================
C/R | Module
---------------------------
 C  | main_func
 C  | add
 R  | main_func
 C  | loop
 C  | loop
 C  | loop
 R  | loop
 R  | loop
 R  | main_func
 R  | collect
```


---
[1]: https://learnku.com/docs/pymotw/trace-follow-program-flow/3467
[2]: https://docs.python.org/zh-cn/3/library/trace.html
[3]: https://blog.csdn.net/u014578266/article/details/89057967