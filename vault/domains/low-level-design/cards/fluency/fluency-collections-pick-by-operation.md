---
id: fluency-collections-pick-by-operation
node: fluency.collections
type: qa
step: 2
---
## Q
要在已处理过的路径里判断“这个路径是否出现过”，输入有重复，还要按首次出现的顺序输出。`list`、`set`、`dict`、`deque` 各适合哪种操作？这个需求该用哪种？

## A
**按最常做的操作选容器**

- **`list`**：按下标取值、尾部追加 O(1)；`x in lst` 和 `lst.pop(0)` 都是 O(n)；要有序、允许重复就用它；
- **`set`**：`x in s`、`add`、`discard` 平均 O(1)；元素必须可哈希，不记顺序、不留重复；
- **`dict`**：键到值的映射，同样 O(1) 查找，并且记住插入序；
- **`deque`**：两端 O(1)（`append`、`popleft`），做队列用它，不要对 `list` 反复 `pop(0)`；
- **“去重且保序”**：`list(dict.fromkeys(items))`，或者边走边用 `seen` 集合判断；只用 `set` 会丢顺序；
- **结果允许重复、还要按固定顺序输出**（如汇率路线里相同数值的多条单次中转），它本来就是序列，用 `list`，别为了“看着去重”换成 `set`。

```python
from collections import deque

def unique_in_order(items):
    return list(dict.fromkeys(items))        # 键唯一，且保持首次出现的位置

print(unique_in_order([3, 1, 3, 2, 1]))      # [3, 1, 2]

seen: set[str] = set()                       # 判断“出现过吗”：O(1)
for p in ["a/b", "a/b", "c"]:
    if p in seen:
        continue
    seen.add(p)
q = deque([1, 2, 3]); q.popleft()            # O(1)，list.pop(0) 是 O(n)
print(sorted(seen), q)                       # ['a/b', 'c'] deque([2, 3])
```

<details class="pt"><summary>延伸</summary>

两个 `set` 做集合运算（`|`、`&`、`-`）可以一行写出“排除集 = 评过的并上看过的”；元素必须可哈希，所以放进去的是 `int`、`str`、`tuple`，不是 `list`、`dict`。

</details>

**知识点：**容器的选择与惯用法（Collections Idioms）
