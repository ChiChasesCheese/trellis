---
id: choose-list-array-memoryview
node: model.sequences
type: qa
source: python-docs
---
## Q
要存一大批同类型数值（比如一百万个整数）时，在 list、`array.array`、`memoryview` 之间应该怎么选？

## A
list 存的是指向独立 Python 对象的指针，最灵活（可以混存任意类型），但每个数值都要付出一份完整 Python 对象的内存和装箱开销；`array.array` 按声明好的 C 类型连续存储原始数值，内存紧凑，适合大批量同质数值，但操作接口不如 list 丰富；`memoryview` 本身不存数据，只是对一段已有的、支持缓冲区协议的内存（如 bytes、bytearray 或 `array.array`）开一个零拷贝窗口，适合在不复制数据的前提下切片、转换格式或跨函数传递一段已有的二进制数据。
