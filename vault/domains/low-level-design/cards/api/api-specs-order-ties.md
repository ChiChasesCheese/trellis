---
id: api-specs-order-ties
node: api.specs
type: qa
step: 5
---
## Q
规格说“返回出现次数最多的 3 个词”，没写平局怎么办、返回什么容器。实现者和测试会在哪里分歧？规格该补什么？

## A
**顺序、平局、容器都属于规格**

- **平局**：次数相同谁先？写成全序的排序键 `(-count, word)`，结果就唯一；
- **容器**：`set` 无序且去重（相同数值会丢），`list` 保留顺序和重复；规格写“升序列表”，实现就别经 `set` 绕一圈；
- **插入序**：`dict` 从 3.7 起保证插入序，但“按插入序”必须写进规格，不能靠巧合；
- **测试**：给出两个平局的输入，断言精确的整个列表，而不是“包含这两个词”。

```python
from collections import Counter

def top_words(words: list[str], k: int) -> list[str]:
    """Returns: up to k words, by count desc, ties by word asc."""
    counts = Counter(words)
    return sorted(counts, key=lambda w: (-counts[w], w))[:k]

print(top_words(["b", "a", "b", "a", "c"], 2))      # ['a', 'b']
print(Counter(["b", "a", "b", "a", "c"]).most_common(2))   # [('b', 2), ('a', 2)]
```

<details class="pt"><summary>延伸</summary>

`Counter.most_common` 的平局按首次出现的顺序排，对“按词升序”的规格是错的，上面两行输出不同正是例子。内置函数的平局行为是它自己的规格，要用就核对它是否等于你的。

</details>

**知识点：**规格与契约（Specifications）
