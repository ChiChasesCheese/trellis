---
id: mlp-traps-py-compare
node: traps.python-output
type: qa
step: 3
---
## Q
**is 与 ==、链式比较、or、元组里的列表**｜语言陷阱与读代码

下面的 Python 代码输出什么？

```python
a = [1]; b = [1]
print(a == b, a is b)
print(1 < 2 < 3, 3 > 2 > 2, 1 == 1 < 2)
print(0 or "x", [] or None, "ab" and "cd")
t = ([1], 2)
try:
    t[0] += [3]
except TypeError:
    print(t)
```

## A
**输出。**
```
True False
True False True
x None cd
([1, 3], 2)
```

- **`==` 与 `is`：** `==` 比较内容，`is` 比较是不是同一个对象；两个内容相同的列表是两个对象。判断是否为 `None` 用 `is None`，比较值用 `==`。
- **链式比较：** `1 < 2 < 3` 展开成 `1 < 2 and 2 < 3`，每个中间值只算一次；`3 > 2 > 2` 是 `3 > 2 and 2 > 2`，为 False；`1 == 1 < 2` 也是链式，为 True。
- **`or` 和 `and` 返回操作数本身：** `or` 返回第一个为真的值，都假则返回最后一个；`and` 返回第一个为假的值，都真则返回最后一个。所以 `0 or "x"` 得 `x`，`[] or None` 得 `None`，`"ab" and "cd"` 得 `cd`。
- **元组里的列表：** `t[0] += [3]` 先让列表原地扩展（成功），再尝试把结果赋回元组的位置（失败），抛 `TypeError`；报错之后元组里的列表已经变了，打印 `([1, 3], 2)`。
- **记住：** 值用 `==`、身份用 `is`；链式比较是 `and`；`or`、`and` 返回的是值，不一定是布尔。

**英文答法。**
- "`==` compares **value**, `is` compares **identity**; for `None` I use `is`."
- "The `+=` mutates the list in place, **then** fails on the tuple assignment."
