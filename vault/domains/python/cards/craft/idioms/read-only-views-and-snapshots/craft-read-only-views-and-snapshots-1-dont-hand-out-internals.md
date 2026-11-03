---
id: craft-read-only-views-and-snapshots-1-dont-hand-out-internals
node: craft.idioms.read-only-views-and-snapshots
type: qa
step: 1
---
## Q
**只读视图与快照 · 为什么 getter 不能直接返回内部列表**｜写法

拼车行程对象有一个 `legs` 属性，内部用 `list` 追加乘客段，同时维护 `seats_taken`。getter 最省事的写法是 `return self._legs`。这样写会在哪里出问题？该怎么改？

## A
**要点。** 返回内部可变容器，等于把对象的不变量（`legs` 的长度和 `seats_taken` 一致）交给了每一个调用方：他们不经过 `add()` 就能直接 `append`。有锁保护的状态更糟，调用方在锁外读写同一个容器。改法是返回**快照**（snapshot）：一份拷贝，之后内部怎么变都不影响它；并且用不可变类型（`tuple`），让调用方想改也改不了。

```python
class LeakyTrip:
    def __init__(self) -> None:
        self._legs: list[str] = ["rider-1"]
        self.seats_taken = 1                  # 与 legs 保持一致才是合法状态

    def add(self, rider: str) -> None:
        self._legs.append(rider)
        self.seats_taken += 1

    @property
    def legs(self) -> list[str]:
        return self._legs                     # 把内部列表直接交出去

class Trip(LeakyTrip):
    @property
    def legs(self) -> tuple[str, ...]:
        return tuple(self._legs)              # 交出去的是拷贝，之后不再变

t = LeakyTrip()
t.legs.append("hacker")                       # 调用方绕过了 add()
print("泄露版: legs =", len(t._legs), "seats_taken =", t.seats_taken, "<- 不变量被破坏")

t = Trip()
try:
    t.legs.append("hacker")                   # type: ignore[attr-defined]
except AttributeError as e:
    print("快照版: 想改也改不了 ->", e)
snap = t.legs
t.add("rider-2")
print("快照不随之后的变化而变:", snap, "| 新快照:", t.legs)
```

实际输出：

```
泄露版: legs = 2 seats_taken = 1 <- 不变量被破坏
快照版: 想改也改不了 -> 'tuple' object has no attribute 'append'
快照不随之后的变化而变: ('rider-1',) | 新快照: ('rider-1', 'rider-2')
```

**为什么。** 类型本身就是约束：`tuple` 没有 `append`，调用方写出来立刻报错，而不是悄悄写进去。一份 `return list(self._legs)` 的拷贝只切断了别名，调用方改自己那份不会出错，但也容易误以为改了对象；用 tuple 把意图写进类型。

**代价。** 每次读都要拷贝 O(n)。读频率高、元素多时见第 5 张卡。
