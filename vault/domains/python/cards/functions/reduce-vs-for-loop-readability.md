---
id: reduce-vs-for-loop-readability
node: functions.functools
type: qa
source: python-docs
---
## Q
`functools.reduce(func, iterable, initial)` 是如何计算出最终结果的？为什么标准库文档建议很多场景下直接写 `for` 循环更清楚？

## A
`reduce` 从左到右把可迭代对象的元素两两累积：先对前两个元素调用 `func`，把结果和第三个元素再调用 `func`，如此持续到耗尽；给了 `initial` 就以它作为第一次计算的起点，也作为可迭代对象为空时的默认返回值，否则空可迭代对象会抛出 `TypeError`。因为整个累积过程被压缩进一次函数调用里，中间状态不可见，换成显式的 `for` 循环虽然多几行，却能让每一步的累积值直接可读、可加日志、可单步调试。
