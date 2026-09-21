---
id: hash-truncated-to-py-ssize-t
node: model.hash-eq
type: qa
source: python-docs
---
## Q
自定义 `__hash__()` 返回的整数会被 CPython 原样使用吗？在常见的 64 位构建上，哈希值实际保留多少字节？

## A
不会原样使用：`hash()` 会把 `__hash__()` 返回的值截断（truncate）到 `Py_ssize_t` 类型的宽度——64 位构建下通常是 8 字节，32 位构建下是 4 字节。如果一个自定义哈希实现需要在不同位宽的构建间保持一致行为，需要显式检查宽度（可以用 `python -c "import sys; print(sys.hash_info.width)"` 查看当前构建的哈希宽度）。
