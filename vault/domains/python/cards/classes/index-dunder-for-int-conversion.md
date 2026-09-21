---
id: index-dunder-for-int-conversion
node: classes.operator-overloading
type: qa
source: python-docs
---
## Q
自定义一个『表现得像整数』的类，为什么应该实现 `__index__()` 而不是只实现 `__int__()`？

## A
`__index__()` 表示『这个数值对象能被无损（losslessly）转换成整数』，Python 在做切片（slicing）、`bin()`、`hex()`、`oct()` 等场合专门找这个方法，只有实现了它才说明该类型确实是一个整数类型，可以安全地用在下标位置。`__int__()` 语义更宽松，允许有精度损失的转换（比如浮点数转 int 会截断），不代表这个值适合当索引用。而且如果 `__int__()`/`__float__()`/`__complex__()` 都没定义，Python 反过来会尝试用 `__index__()` 兜底，说明 `__index__()` 在数值协议里的地位更基础。
