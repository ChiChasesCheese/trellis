---
id: pl-foundations-execution-models-found-cpython-pyc
node: foundations.execution-models
type: qa
step: 3
---
## Q
CPython 运行一个 `.py` 文件时，源码在什么时候被编译？`__pycache__` 里的 `.pyc` 文件是什么？

## A
CPython 不直接解释源码文本。每次导入一个模块时，它先把源码编译成代码对象（code object，里面是字节码，一串面向栈的指令），再由解释器的求值循环逐条执行。编译很快，所以对用户不可见。

为了避免重复编译，导入的模块会把编译结果缓存到 `__pycache__/名字.cpython-314.pyc`（文件名里带解释器版本）。下次导入时，如果源文件的修改时间和大小没变，就直接读缓存。

```python
# main.py          # mod.py: def f(): return 1
import mod
print(mod.f())
```

运行 `python3 main.py` 输出 `1`，并且目录里多出 `__pycache__/mod.cpython-314.pyc`。注意入口脚本 `main.py` 本身不会被缓存，只有被 `import` 的模块才会。

两点认识：`.pyc` 是纯粹的启动优化，删掉它只会让下一次导入慢一点，不会改变行为；它也不是可移植的「编译产物」，不同 Python 版本的字节码互不兼容。另外，这一步只做语法分析，所以语法错误在导入时就会暴露，而名字写错之类的错误要等到那行代码执行时才暴露。
