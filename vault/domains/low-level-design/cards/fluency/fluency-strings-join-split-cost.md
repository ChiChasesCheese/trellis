---
id: fluency-strings-join-split-cost
node: fluency.strings-bytes
type: qa
step: 6
---
## Q
付款串 `"2026-11-17, 500, alice, rent, Q4, paid"` 要切成日期、金额、付款人、备注（备注里可能有逗号）。`split` 怎么写才不会把备注切碎？拼接大量字符串时 `+=` 和 `join` 的区别是什么？

## A
**`split` 限制次数；拼接用 join**

- **`split(sep, maxsplit)`**：`s.split(", ", 3)` 最多切 3 刀，备注留在最后一段，逗号保持原样；不限制就会把备注拆成几段，字段数也随之变化；
- **`split()` 不带参数按空白切并丢掉空串**：`"a  b".split()` 是 `["a", "b"]`；`split(" ")` 保留空串，`["a", "", "b"]`；两者行为不同，要按需求选；
- **`partition(sep)` 只切第一处**，返回三元组，找不到分隔符时后两项是空串，不用判断异常；
- **`+=` 在循环里**：`str` 不可变，每次拼接生成新对象，整体是平方级的复制；CPython 对单引用的情况有优化，但那是实现细节，换别的实现就慢；
- **`"".join(parts)`**：先收集成 `list`，一次拼完，线性；`join` 的元素必须全是 `str`，传 `int` 抛 `TypeError`，要先 `map(str, …)`；
- **格式化**：f-string 可读又快；格式规格写在冒号后，`{x:.2f}`、`{n:06}`、`{n:,}`；日志里用 `%s` 延迟格式化，别提前拼好。

```python
line = "2026-11-17, 500, alice, rent, Q4, paid"
date, amount, payer, note = line.split(", ", 3)
print(note)                                         # rent, Q4, paid：逗号保留
print("a  b".split(), "a  b".split(" "))            # ['a', 'b'] ['a', '', 'b']
print("a=b=c".partition("="), "abc".partition("="))   # ('a','=','b=c') ('abc','','')

parts = [str(i) for i in range(5)]
print(",".join(parts), f"{1234567:,} {0.256:.1%} {42:06}")   # 0,1,2,3,4 1,234,567 25.6% 000042
```

**知识点：**字符串与字节（Strings & Bytes）
