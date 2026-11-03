---
id: craft-dunder-protocols-that-pay-4-container-protocols
node: craft.idioms.dunder-protocols-that-pay
type: qa
step: 4
---
## Q
**特殊方法 · 让自定义容器像内置容器一样可用要写哪几个方法**｜写法

环形队列想支持 `len(x)`、`k in x`、`for v in x`，让使用者像用内置容器一样用它。需要写哪些特殊方法？哪些可以不写，Python 会退回到别的方法？

## A
**要点。** `len()`、`in`、`for` 和真值判断各对应一个特殊方法：`__len__`、`__contains__`、`__iter__`、`__bool__`。没写 `__bool__` 时 `bool(x)` 退回 `__len__`（长度为零就是假）；没写 `__contains__` 时 `in` 退回 `__iter__` 逐个比较。所以最少写 `__len__` 和 `__iter__`，其他行为随之而来。`__iter__` 要按使用者期待的顺序（队列顺序），而不是内部数组的顺序。

```python
class Ring:
    """固定容量的环形队列。"""
    def __init__(self, k: int) -> None:
        self._buf: list[int | None] = [None] * k
        self._head = self._n = 0
    def push(self, x: int) -> bool:
        if self._n == len(self._buf):
            return False
        self._buf[(self._head + self._n) % len(self._buf)] = x
        self._n += 1
        return True
    def pop(self) -> int:
        x = self._buf[self._head]
        self._head = (self._head + 1) % len(self._buf)
        self._n -= 1
        return x                                # type: ignore[return-value]
    def __len__(self) -> int: return self._n
    def __iter__(self):                         # 按队列顺序，而不是数组顺序
        for i in range(self._n):
            yield self._buf[(self._head + i) % len(self._buf)]

r = Ring(3)
for x in (1, 2, 3): r.push(x)
r.pop(); r.push(4)                              # 数组内部是 [4, 2, 3]
print(len(r), list(r), 4 in r, bool(r))
r2 = Ring(2)
print(bool(r2), r2.push(9), bool(r2))           # 没写 __bool__：由 __len__ 决定
```

实际输出：

```
3 [2, 3, 4] True True
False True True
```

**为什么。** 第一行：内部数组是 `[4, 2, 3]`，迭代结果是 `[2, 3, 4]`，因为 `__iter__` 从队头开始走；`4 in r` 没写 `__contains__`，是退回到迭代得到的。第二行：空队列为假，放入一个后为真，没有写 `__bool__`。

**信号。** 使用者本来会写 `len(x)` / `k in x` 的类型，就实现这几个方法。`in` 退回迭代是 O(n)；需要更快时再单独写 `__contains__`。
