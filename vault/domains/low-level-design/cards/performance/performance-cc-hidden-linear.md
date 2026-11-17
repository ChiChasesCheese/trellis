---
id: performance-cc-hidden-linear
node: performance.complexity-constants
type: qa
step: 2
---
## Q
代码里没有嵌套循环，只有一层 `for`，循环体里写了 `if x in seen_list`、`items.insert(0, x)`、`copy = items[:]`。为什么整体仍然是 O(n²)？哪些写法看着像一步，其实是 O(n)？

## A
**循环里每个看似一步的操作，都要问“它自己是几次元素操作”**

- **`x in list`、`list.index`、`list.remove`**：从头扫描，找不到时扫完整个列表；
- **`insert(0, x)`、`pop(0)`、`del l[0]`**：后面所有元素整体移位；
- **`l[:]`、`list(l)`、`sorted(l)`**：复制或排序整个序列，放进循环里就是 n 次整体复制；
- **O(1) 的例子**：`len(l)`、`l.append`、`l[i]`、`d[k]`、`x in set`；
- **嵌套循环不是唯一的二次方来源**：隐含的线性操作放在一层循环里，总量同样是 n × n。

实测（3.11，本机，每次调用的耗时）：

| 操作 | n=1,000 | n=10,000 | n=100,000 |
|---|---|---|---|
| `-1 in l`（找不到） | 2.3 µs | 23 µs | 236 µs |
| `l.insert(0, 1); l.pop(0)` | 0.16 µs | 1.5 µs | 21 µs |
| `l[:]` | 0.52 µs | 9.0 µs | 96 µs |
| `len(l)` | 约 10 ns | 约 9 ns | 约 9 ns |

表里的数字有两个读法：同一个操作，规模扩大 10 倍，耗时也大约扩大 10 倍，这就是线性；`len` 不随规模变化，这就是常数。下面是按这个数推算的结果（乘法，非实测）：在 10 万个请求里每个都 `in` 一个 10 万元素的列表，约 10 万 × 236 µs ≈ 24 秒。

```python
def dedupe_slow(items):
    seen, out = [], []
    for x in items:
        if x not in seen:       # 隐含的线性扫描：整体 O(n²)
            seen.append(x); out.append(x)
    return out

def dedupe(items):
    return list(dict.fromkeys(items))    # 一遍，保持首次出现的顺序

print(dedupe([3, 1, 3, 2, 1]), dedupe_slow([3, 1, 3, 2, 1]))   # [3, 1, 2] [3, 1, 2]
```

**知识点：**复杂度与常数（Complexity vs Constants）
