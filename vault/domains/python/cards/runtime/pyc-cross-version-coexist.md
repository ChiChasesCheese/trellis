---
id: pyc-cross-version-coexist
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
同一份源码分别用 Python 3.11 和 3.13 运行，两者在 `__pycache__` 里生成的编译缓存会互相覆盖或用错吗？

## A
不会。`.pyc` 文件名里编码了解释器实现和版本号（如 `spam.cpython-311.pyc` / `spam.cpython-313.pyc`），不同版本各自生成、各自命名，同放在一个 `__pycache__` 目录下也不冲突，每个解释器只认自己版本号对应的那份缓存。
