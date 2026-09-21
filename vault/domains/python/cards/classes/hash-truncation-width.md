---
id: hash-truncation-width
node: classes.pythonic-object
type: qa
source: python-docs
---
## Q
自定义 `__hash__()` 返回的整数会不会原样被 `hash()` 使用？在 64 位构建的 CPython 上，`hash()` 的返回值实际按多宽截断？

## A
不会原样使用：`hash()` 会把自定义 `__hash__()` 返回的整数截断到 `Py_ssize_t` 的宽度。在 64 位构建上这是 8 字节（32 位构建上是 4 字节），可用 `sys.hash_info.width` 查询。这意味着跨位宽环境互操作的类要注意自己的哈希值不能依赖超出这个宽度的精度。
