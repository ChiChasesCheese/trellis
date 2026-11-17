---
id: performance-cc-move-loop-to-c
node: performance.complexity-constants
type: qa
step: 5
---
## Q
统计 50 万个词的出现次数，手写 `d[w] = d.get(w, 0) + 1` 和 `collections.Counter(words)`，两者都是 O(n)，为什么耗时差一截？同样的大 O 下，常数从哪里省？

## A
**同样 O(n)，把循环交给 C 实现，常数更小**

- **解释器的循环每一步都有开销**：取下一个元素、执行字节码、调用 `get`、写回字典；
- **`Counter(iterable)` 的计数循环在 C 里**：省掉每个元素的字节码解释；
- **同类的内置**：`sum`、`min`、`max`、`sorted(key=...)`、`str.join`、`dict.fromkeys`、列表推导式，都比手写循环快一截；
- **别神化**：差距是 20% 到几倍，不是几个数量级；数量级要靠换算法，不是换写法；
- **先写清楚，再测**：这类改写只在热点上做，热点要先量出来（见剖析那张卡）。

实测（3.11，本机，50 万个词，5000 种）：

| 写法 | 耗时 |
|---|---|
| `Counter(words)` | 9.9 ms |
| 手写 `d.get(w, 0) + 1` | 12.4 ms |
| `defaultdict(int)` 里 `d[w] += 1` | 13.0 ms |

```python
import random, timeit
from collections import Counter

words = [str(random.randrange(5000)) for _ in range(500_000)]

def manual():
    d = {}
    for w in words: d[w] = d.get(w, 0) + 1
    return d

assert Counter(words) == manual()      # 结果一样，只有常数不同
for f in (lambda: Counter(words), manual):
    print(round(min(timeit.repeat(f, number=1, repeat=5)) * 1000, 1), "ms")
```

**知识点：**复杂度与常数（Complexity vs Constants）
