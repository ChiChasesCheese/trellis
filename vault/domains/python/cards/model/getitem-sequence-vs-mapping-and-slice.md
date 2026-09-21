---
id: getitem-sequence-vs-mapping-and-slice
node: model.dunder-protocols
type: qa
source: python-docs
---
## Q
`__getitem__(self, subscript)` 既要支持 `seq[2]` 这样的整数下标，又要支持 `d["key"]` 这样的字典取值，解释器如何区分？切片赋值 `a[1:2] = b` 底层怎么翻译成方法调用？

## A
`__getitem__` 本身不区分「序列」还是「映射」语义，由实现者决定 `subscript` 该被当成整数/`slice` 对象（序列语义）还是任意可哈希的键（映射语义）：下标类型不对应抛 `TypeError`，下标值不合法应抛 `LookupError` 的子类（序列用 `IndexError`、映射用 `KeyError`）。切片语法会被解释器翻译成显式的 slice 对象调用：`a[1:2] = b` 等价于 `a[slice(1, 2, None)] = b`，缺省的切片位置一律用 `None` 填充后交给 `__setitem__` 处理。
