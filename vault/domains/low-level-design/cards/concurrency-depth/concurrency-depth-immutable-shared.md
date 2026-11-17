---
id: concurrency-depth-immutable-shared
node: concurrency-depth.confinement
type: qa
step: 1
---
## Q
要把一份通知对象给多个线程同时读，不想加锁。`@dataclass(frozen=True)` 够用吗？“不可变”到什么程度才真的不用锁？

## A
**不可变的值可以随便共享，但 frozen 只冻结一层**

- **为什么不用锁**：没人能改的对象，读线程之间没有冲突，也没有“读到一半”的状态；想改就造一个新对象，旧的原样留给还在读的线程；
- **`frozen=True` 是浅的**：属性不能重新赋值，但属性指向的 `list`、`dict` 还能改。字段里放了列表，等于把可变状态藏进了“不可变”对象；
- **字段也要不可变**：`tuple`、`frozenset`、`str`、数字，或者别的 frozen 对象；
- **编辑 = 造新值**：`dataclasses.replace(n, tags=n.tags + ("hot",))`；
- **含 `list` 字段还会让 `hash()` 抛 `TypeError`**：frozen 加 `eq` 会生成 `__hash__`，哈希要遍历字段。

```python
from dataclasses import dataclass, replace
@dataclass(frozen=True)
class Notice:
    movie: str
    tags: tuple[str, ...] = ()
n = Notice("m1", ("new",))
n2 = replace(n, tags=n.tags + ("hot",))
print(n.tags, n2.tags)                     # ('new',) ('new', 'hot')
@dataclass(frozen=True)
class Leaky:
    tags: list
x = Leaky(["a"]); x.tags.append("b")
print(x.tags)                              # ['a', 'b']：浅冻结拦不住
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）
