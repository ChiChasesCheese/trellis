---
id: frame-per-thread-stack-allocation
node: runtime.frames-eval
type: qa
source: cpython-internals
---
## Q
调用一个 Python 函数时，解释器在哪里给这次调用的帧（frame）分配内存？为什么不能直接分配在 C 的调用栈上？

## A
Python 语义允许帧在函数调用结束后继续存活（比如被回溯 traceback 或 `sys._getframe()` 引用），而 C 栈帧一返回就失效，所以不能借用 C 调用栈。CPython 把绝大多数帧连续分配在「每个线程自己的一段栈」（per-thread stack）里，兼顾了避免逐帧堆分配的开销和良好的内存局部性；只有生成器/协程的帧例外——直接内嵌在生成器对象里。
