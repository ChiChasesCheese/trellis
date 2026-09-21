---
id: functions-as-first-class-objects
node: functions.first-class
type: qa
source: python-docs
---
## Q
在 Python 里说函数是「一等对象」（first-class object）具体指什么？请举一个把函数当作参数传递的例子。

## A
指函数和整数、字符串一样，可以被赋值给变量、存入列表/字典、作为参数传给其他函数、也可以被函数返回。例如 `sorted(items, key=len)` 把内置函数 `len` 直接传给 `sorted` 的 `key` 参数，不需要额外包装成别的形式。
