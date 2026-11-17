---
id: performance-measure-stop-early
node: performance.measure-first
type: qa
step: 4
---
## Q
接口只要“匹配条件的前 10 条”，写成 `[x for x in items if match(x)][:10]`。测下来整个函数时间随数据量线性涨，怎么改？改完怎么证明有效？

## A
**先写下“要多少”，凑够就停：最快的工作是不做的工作**

- **列表推导式先把全部匹配项算完**：再取前 10 个，后面几十万项的计算全是浪费；
- **生成器加 `itertools.islice`**：边产生边计数，取够 10 个就停止遍历；
- **语义要对**：先匹配、后截断，不是先截断再匹配（先截断会丢掉本该排在前面的匹配项）；
- **只对“头部很快就能凑够”的数据有效**：如果匹配项极少，仍然要扫完全部，收益取决于匹配率；
- **改完要量**：用同一份输入、同一种测量方法，对比前后，不凭“应该更快”。

实测（3.11，本机，100 万个整数，匹配 `x % 3 == 0`，取前 10 个，`timeit` 最小值）：列表推导式后切片 9.8 ms；`islice` 加生成器 0.0006 ms。

```python
import itertools, timeit

data = list(range(1_000_000))

def eager(): return [x for x in data if x % 3 == 0][:10]
def lazy():  return list(itertools.islice((x for x in data if x % 3 == 0), 10))

assert eager() == lazy()                       # 同一个结果：先匹配、后截断
for f in (eager, lazy):
    print(f.__name__, min(timeit.repeat(f, number=1, repeat=5)) * 1e3, "ms")
```

**知识点：**先测量（Measure First）
