---
id: uth-python-str-int-2-intern
node: python.str-int
type: qa
step: 2
---
## Q
**is 为什么有时对、有时错**｜Python · CPython 3.14

`int('256') is int('256')` 为 `True`，`int('257') is int('257')` 为 `False`；字符串也有类似现象，这是怎么回事？

## A
**结构。** 解释器预先建好并共享一批不可变对象：小整数缓存 -5 到 256，以及驻留（interning）字符串表。

**细节。**

- 实测 `int('-5') is int('-5')` 为真，`int('-6') is int('-6')` 为假。
- 运行时拼出的 `'hello_world'` 与字面量不是同一个对象；`sys.intern` 后才相同。
- 标识符、属性名自动驻留。

**为什么。** 驻留后 `dict` 查属性名时，哈希相同再比一次指针就够，不用逐字符比较。

**坑。** 比较值永远用 `==`，`is` 只用于 `None`。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 205 同构字符串
