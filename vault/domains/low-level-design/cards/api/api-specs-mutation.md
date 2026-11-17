---
id: api-specs-mutation
node: api.specs
type: qa
step: 6
---
## Q
“对列表排序并返回前三项”的函数，规格没写会不会改传入的列表。调用方会被什么坑到？规格怎么写？

## A
**后置条件要写明改了什么、没改什么**

- **不只是返回值**：被改的参数、全局状态、对象字段都在后置条件里（常叫 modifies 子句或 frame condition）；
- **容易选错的一对**：`list.sort()` 原地改并返回 `None`，`sorted()` 返回新列表；写错的函数让调用方的列表被悄悄重排；
- **默认**：函数不改入参，除非名字和文档明说（如 `sort_in_place`）；
- **测试**：调用前复制一份，调用后断言入参与副本相等。

```python
def top3(xs: list[int]) -> list[int]:
    """Returns: the 3 largest, desc. Does not modify xs."""
    return sorted(xs, reverse=True)[:3]

def top3_bad(xs: list[int]) -> list[int]:
    xs.sort(reverse=True)               # 调用方的列表被重排
    return xs[:3]

data = [2, 9, 4, 7]
before = list(data)
top3(data)
print(data == before)       # True
top3_bad(data)
print(data == before)       # False
```

**知识点：**规格与契约（Specifications）
