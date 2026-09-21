---
id: runtime-concat-breaks-is-comparison
node: model.names-objects
type: qa
source: cpython-internals
---
## Q
```python
a = "hello_world"
b = "hello_world"
print(a is b)
```
在同一个函数体里这段代码通常打印 True；但如果把 `b` 改成用切片、`input()` 或非常量折叠的方式在运行时拼接出同样内容，`a is b` 却常常变成 False，为什么？

## A
两个字面量在同一段代码里会被编译器当作同一个常量编译进代码对象并驻留成一个对象，所以 `is` 为 True；而运行时拼接（切片、字符串加法变量、外部输入）产生的字符串是新分配、未驻留的对象，即使内容相同，`is` 比较的是内存地址而非内容，结果为 False。用 `is` 判断字符串内容是否相同是常见的隐藏 bug 来源。
