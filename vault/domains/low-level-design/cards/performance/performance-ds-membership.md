---
id: performance-ds-membership
node: performance.data-structures
type: qa
step: 1
---
## Q
服务里有一个 `blocked_ids` 列表，每个请求都要判断 `user_id in blocked_ids`。规模从一百涨到十万，这行代码为什么会从“看不出来”变成“CPU 全花在这里”？换成什么，什么时候不值得换？

## A
**判断“在不在”：list 是扫描，set 是哈希查找**

- **`in` 对 list 是线性扫描**：平均要比较 n/2 次，耗时跟着长度涨；
- **`in` 对 set / dict 是哈希查找**：平均 O(1)，十万个元素和一百个元素耗时几乎一样；
- **建集合有成本**：一次性建 10 万元素的 set 要几百微秒，查询次数少于几次就回不了本；
- **set 不保序、元素必须可哈希**：要保持插入顺序用 `dict.fromkeys(items)`；要存列表这类不可哈希的东西，先转成元组；
- **按访问模式选**：建一次、查很多次 → set；只遍历、只查一两次 → 留着 list。

实测（3.11，本机，`timeit`，每次查询的平均耗时）：

| 元素个数 | `x in list` | `x in set` |
|---|---|---|
| 100 | 144 ns | 6 ns |
| 10,000 | 13,084 ns | 10 ns |
| 100,000 | 138,051 ns | 11 ns |

```python
import timeit, random
data = list(range(100_000)); s = set(data)
probes = [random.randrange(100_000) for _ in range(1000)]
for name, c in (("list", data), ("set", s)):
    t = min(timeit.repeat("for p in probes: p in c", globals={"probes": probes, "c": c},
                          number=20, repeat=5))
    print(name, round(t / 20 / 1000 * 1e9), "ns/查询")
```

<details class="pt"><summary>延伸</summary>

`set(data)` 本身 100,000 个元素要约 308 µs，等于约 2 次 list 查询的代价，所以同一批数据只要查超过两三次，先建 set 就划算。真正危险的是它藏在循环里：10 万个请求每个扫一遍 10 万元素的列表，就是 10¹⁰ 次比较。

</details>

**知识点：**按访问模式选结构（Choosing Structures）
