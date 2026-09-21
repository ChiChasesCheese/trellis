---
id: int-arbitrary-precision
node: model.numbers
type: qa
source: python-docs
---
## Q
Python 的 `int` 能表示的数值范围受什么限制？和固定宽度的 C 整数类型有什么本质不同？

## A
Python 的 `int` 是任意精度（arbitrary precision）整数：它代表的是不限范围的数学整数集合，唯一的限制是可用的（虚拟）内存，而不是像 C 的 `int32`/`int64` 那样有固定的比特宽度上限。这意味着做大数运算（比如计算很大的阶乘）不会像固定宽度整数那样发生溢出（overflow）回绕，但数值越大，底层占用的内存和运算耗时也会相应增长。
