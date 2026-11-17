---
id: data-defensive-copy-in-and-out
node: data.defensive-copy
type: qa
step: 1
---
## Q
`Roster(names)` 的构造函数把传入的列表直接存成 `self._names`，`roster.names()` 又直接返回它。调用方在哪两个时刻能绕过类的校验？防御性拷贝（defensive copy）要在哪两个方向做？

## A
**进来复制一次，出去复制一次**

- **进来**：构造函数保存的是调用方的那个列表对象；之后他 `names.append("")`，类内部就多了一个从未校验过的元素；
- **出去**：`names()` 返回内部列表，调用方 `r.names().clear()` 直接清空内部状态；
- **两个方向都要**：只拦一边，另一边就是后门；
- **复制的时机**：在校验之前复制，再校验这份副本；校验完调用方改原列表就影响不到你；
- **同类陷阱**：可变默认参数 `def __init__(self, names=[])`，所有实例共享同一个列表。

```python
class Roster:
    def __init__(self, names: list[str]):
        self._names = list(names)                  # 进来：先复制
        if not all(n.strip() for n in self._names):    # 再校验这份副本
            raise ValueError("blank name")
    def names(self) -> list[str]:
        return list(self._names)                   # 出去：返回副本

src = ["ann", "bo"]
r = Roster(src)
src.append("")                                     # 改原列表，不影响 r
r.names().clear()                                  # 改返回值，不影响 r
print(r.names())
```

**知识点：**防御性拷贝（Defensive Copying）
