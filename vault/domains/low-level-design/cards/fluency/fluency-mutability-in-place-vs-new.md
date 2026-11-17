---
id: fluency-mutability-in-place-vs-new
node: fluency.mutability
type: qa
step: 5
---
## Q
`top_two(items)` 里写了 `items.sort()` 再返回 `items[:2]`，调用方发现自己传进去的列表顺序变了。`sort()` 和 `sorted()`、`a += [x]` 和 `a = a + [x]` 有什么区别？函数该怎么对待参数？

## A
**函数默认不改参数；要排序就用 sorted**

- **原地方法返回 `None`**：`list.sort()`、`reverse()`、`append()`、`extend()` 改原对象，返回 `None`；`x = xs.sort()` 得到 `None`；
- **返回新对象的写法**：`sorted(xs)`、`list(reversed(xs))`、`xs + [x]`，原列表不动；
- **`a += [x]` 对列表是原地的**（相当于 `extend`），所有指向它的名字都看见；`a = a + [x]` 建新列表并重新绑定；对元组、字符串，`+=` 等价于新建；
- **调用方不期待被修改**：函数没有写明“会就地修改”，就当参数只读；先复制、`sorted` 或构造新列表，再处理；
- **如果确实要原地改**：名字和文档要说明（`sort_in_place`、`mutate`），并且不返回值，免得调用方以为拿到了新对象；
- **测试**：调用前后比较输入有没有变，`assert data == [3, 1, 2]`。

```python
def top_two_bad(items):
    items.sort()                     # 调用方的列表被排序了
    return items[:2]

def top_two(items):
    return sorted(items)[:2]         # 新列表，参数不动

data = [3, 1, 2]
top_two(data); print(data)           # [3, 1, 2]
top_two_bad(data); print(data)       # [1, 2, 3]

a = [1]; b = a; a += [2]; print(b)               # [1, 2]：原地
a = [1]; b = a; a = a + [2]; print(b, a)         # [1] [1, 2]：新对象
```

**知识点：**可变性与别名（Mutability & Aliasing）
