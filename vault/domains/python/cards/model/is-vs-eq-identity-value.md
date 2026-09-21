---
id: is-vs-eq-identity-value
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
在 CPython 中，比较两个名字（name）时，`is` 与 `==` 分别检查什么？为什么同样内容的两个变量可能一个用 `is` 判断为 False、用 `==` 判断为 True？

## A
`is` 比较两个名字绑定的对象身份（identity），即 `id()` 返回的地址是否相同；`==` 调用左操作数的 `__eq__` 比较值（value）。两次独立构造出的内容相同的对象（如两次拼接得到的同一字符串）身份不同但值相等，所以 `is` 为 False 而 `==` 为 True。
