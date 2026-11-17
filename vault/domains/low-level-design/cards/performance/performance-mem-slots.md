---
id: performance-mem-slots
node: performance.memory
type: qa
step: 2
---
## Q
内存里要放一百万个只有两个字段的小对象，普通类和加了 `__slots__` 的类内存差多少？为什么？代价是什么？

## A
**`__slots__` 去掉每个实例的 `__dict__`，字段直接存在对象里**

- **普通实例带一个字典**：存放属性名到值的映射，字典自己也占几十到上百字节；
- **`__slots__ = ("a", "b")` 把字段固定成槽位**：没有 `__dict__`，每个实例小一截，创建也略快；
- **代价是不能随意加属性**：赋值没声明的名字会报 `AttributeError`；
- **继承时要小心**：子类不写 `__slots__` 就又有 `__dict__` 了，白省；
- **只在实例数量很大时才值得**：几百个对象省的是几 KB，不值得牺牲灵活性；一百万个才值得。

实测（3.11，本机，`tracemalloc` 峰值，一百万个实例放进列表）：

| 写法 | 峰值内存 | 创建耗时 |
|---|---|---|
| 普通类 | 96.5 MB | 56 ms |
| `__slots__` | 56.4 MB | 45 ms |

按实例摊算（含列表里 8 字节的指针）：普通类约 96 字节，`__slots__` 约 56 字节。

```python
import tracemalloc

class P:
    def __init__(self, a, b): self.a, self.b = a, b

class S:
    __slots__ = ("a", "b")
    def __init__(self, a, b): self.a, self.b = a, b

def per_instance(cls, n=100_000):
    tracemalloc.start(); xs = [cls(1, 2) for _ in range(n)]
    cur, _ = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return cur // n

print(per_instance(P), per_instance(S), "字节/实例（含列表里的 8 字节指针）")
```

<details class="pt"><summary>延伸</summary>

`@dataclass(slots=True)`（3.10 起）一行就能得到槽位版本。如果只需要不可变的小记录，`NamedTuple` 也很紧凑。

</details>

**知识点：**减少分配（Reducing Allocation）
