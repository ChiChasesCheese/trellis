---
id: pl-rt-ffi-found-python
node: runtime.ffi
type: qa
step: 5
---
## Q
Python 有哪几种调用 C 或 Rust 的方式？`ctypes`、C 扩展（C API）和 PyO3 的区别是什么？
为什么 Python 生态严重依赖它们？

## A
Python 本身慢（解释执行），但 FFI 做得很好，使它成了“胶水语言”。三种主要方式：

1. **`ctypes`**（标准库）：运行时直接加载共享库并调用，无需编译：
```python
libc = ctypes.CDLL(None)                       # symbols of the current process / libc
libc.strlen.argtypes = [ctypes.c_char_p]
libc.strlen.restype = ctypes.c_size_t
print(libc.strlen(b"hello, ffi"))              # 10
```
输出：`10`。优点是零构建、写起来快；缺点是类型全靠你声明，慢、容易出错。

2. **C 扩展 / Python C API**：用 C 写模块，使用 `Python.h` 提供的函数（`PyObject*`、`PyArg_ParseTuple`），编译成 `.so` 让 Python `import`。NumPy、pandas 的核心都是这种形式。优点：最灵活、能直接操作 Python 对象；缺点：要手动管理引用计数，写错就崩溃或泄漏。它也是 CPython 难以演进的原因（扩展依赖解释器内部细节）。

3. **绑定生成器**：Cython（把类 Python 语法编译成 C 扩展）、cffi、pybind11（C++）、**PyO3**（Rust）。PyO3 让你用 Rust 写函数并加一个属性宏，它自动完成 Python 对象与 Rust 类型的转换、引用计数、GIL 的持有与释放，用 `maturin` 构建。如今新的高性能库（Polars、Ruff、pydantic-core）大多用 Rust + PyO3 写。

心智模型：Python 对象本质上是 C 里的 `PyObject*`，所以 Python 调用 C 是“**自己人**”的调用：不需要像 Java、Go 那样重新翻译整个对象模型。代价是每次调用都有解释器层面的开销：参数打包成元组、类型检查、转换。
