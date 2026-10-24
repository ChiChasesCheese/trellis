---
id: tlc-python-classes-design-6-dunder
node: python.classes-design
type: qa
step: 6
---
## Q
**Python 设计题｜`__eq__` / `__hash__` / `__repr__` 与容器协议**

自定义类放进 `set` 或当字典键时要满足什么？调试时 `print(node)` 打印出一串地址，怎么办？

## A
**可哈希**要求 `__eq__` 和 `__hash__` 同时一致：相等的对象必须有相同的哈希值。只定义 `__eq__` 会让类变成**不可哈希**。

```python
class Pt:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
    def __eq__(self, o: object) -> bool:
        return isinstance(o, Pt) and (self.x, self.y) == (o.x, o.y)
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    def __repr__(self) -> str:
        return f"Pt({self.x}, {self.y})"
print({Pt(1, 2), Pt(1, 2)}, Pt(1, 2))   # {Pt(1, 2)} Pt(1, 2)
class Q:
    def __eq__(self, o: object) -> bool: return True
try:
    {Q()}
except TypeError as e:
    print(e)    # cannot use 'Q' as a set element (unhashable type: 'Q')
```

- 不想写这些：用 `@dataclass(frozen=True)`，三个方法自动生成；或直接用元组 `(x, y)` 当键。
- `__repr__` 决定调试时看到什么；`print(root)` 打印 `<TreeNode object at 0x...>` 没用，给链表、树节点写一个 `__repr__`，调试效率差很多。
- 容器协议，设计题（LC 706 设计哈希映射、LC 705）里偶尔要求像容器一样用：
  - `__len__` → `len(obj)`
  - `__contains__` → `x in obj`
  - `__getitem__` / `__setitem__` → `obj[k]`、`obj[k] = v`
  - `__iter__` → `for x in obj`
- LeetCode 的设计题固定接口（`get`、`put`），一般不需要这些魔术方法；写出来只在面试官追问「你想让它像 `dict` 一样用呢」时有加分。
- **坑**：对象放进 `set` / 当键之后，**不要再修改参与哈希的字段**，否则再也找不到它。
