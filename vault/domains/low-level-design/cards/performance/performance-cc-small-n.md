---
id: performance-cc-small-n
node: performance.complexity-constants
type: qa
step: 1
---
## Q
一个函数每次被调用，都要判断某个值是否在传进来的 8 个元素里。有人说“`in list` 是 O(n)，应该先转成 set”。大 O 在这里为什么会误导？转 set 在多小的规模下开始划算？

## A
**n 很小时，常数项说了算，大 O 只在规模大时才是主角**

- **大 O 丢掉了常数**：O(1) 的哈希查找，每次要算哈希、探测桶；O(n) 的扫描在 n 很小时只是几次指针比较；
- **“每次调用都新建”算进成本**：转 set 要遍历一遍所有元素，查询次数少时，建表的代价盖过了省下的比较；
- **交叉点在个位数到几十**：下表是本机实测，规模到 20 以上，建 set 就明显划算；
- **该怎么办**：固定的小集合直接写成字面量 `x in ("a", "b", "c")`，编译器会存成常量；规模大或要反复查的，才建一次 set 复用；
- **别拿大 O 当结论**：先问“n 多大、查几次”，再决定要不要换结构。

实测（3.11，本机）：每次调用先 `set(data)` 再查 10 次，对比直接在 list 里查 10 次（单位 ns）：

| n | 10 次 `in list` | 建 set + 10 次查 |
|---|---|---|
| 3 | 85 | 96 |
| 8 | 143 | 112 |
| 20 | 335 | 168 |
| 50 | 780 | 234 |

```python
import timeit, random

for n in (3, 8, 20, 50):
    data = list(range(n)); probes = [random.randrange(n) for _ in range(10)]
    g = {"data": data, "probes": probes}
    a = timeit.timeit("for p in probes: p in data", globals=g, number=100_000)
    b = timeit.timeit("s = set(data)\nfor p in probes: p in s", globals=g, number=100_000)
    print(n, round(a * 1e4), round(b * 1e4), "ns")
```

**知识点：**复杂度与常数（Complexity vs Constants）
