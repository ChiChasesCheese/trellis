---
id: array-typecode-compact-storage
node: model.sequences
type: qa
source: python-docs
---
## Q
`array` 模块的数组存同样数量的数值为什么比 list 更省内存？它靠什么机制做到紧凑（compact）存储？

## A
`array.array` 在创建时用一个字符组成的 typecode（类型码）声明元素对应的 C 层类型，例如 `'b'` 对应 signed char（最小 1 字节）、`'l'` 对应 signed long（最小 4 字节）、`'q'` 对应 signed long long（最小 8 字节），数组内部就按这个固定宽度连续存储原始数值本身。而 list 存的是指向一个个独立 Python 对象的指针（每个 int/float 都是带类型指针和引用计数的完整对象），元素越多这份「每个元素都是一个对象」的开销越明显；array 用固定宽度的原始数值连续存储，省掉了这层逐元素装箱（boxing）开销，所以更紧凑。
