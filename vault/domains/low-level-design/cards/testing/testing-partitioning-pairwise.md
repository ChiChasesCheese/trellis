---
id: testing-partitioning-pairwise
node: testing.partitioning
type: qa
step: 2
---
## Q
一个服务要在 4 个 Python 版本 × 3 种数据库 × 4 种批大小 × 3 种操作系统上验证，全组合是 144 套环境，每套要跑 20 分钟。怎么在可接受的成本下覆盖得足够好？两两组合测试（pairwise testing）是什么，它的依据和局限是什么？

## A
**两两组合：选一组配置，使任意两个参数的任意取值组合都至少出现一次。这里 18 套就够，而全组合是 144 套。**

```python
from itertools import combinations, product

def pairwise(params):
    names = list(params)
    uncovered = {((a, va), (b, vb))
                 for a, b in combinations(names, 2)
                 for va in params[a] for vb in params[b]}
    rows = []
    while uncovered:
        # greedy: the full combination that covers the most new pairs
        best = max(product(*params.values()), key=lambda row: sum(
            ((a, row[i]), (b, row[j])) in uncovered
            for (i, a), (j, b) in combinations(enumerate(names), 2)))
        row = dict(zip(names, best))
        uncovered -= {((a, row[a]), (b, row[b]))
                      for a, b in combinations(names, 2)}
        rows.append(row)
    return rows

matrix = {"python": ["3.11", "3.12", "3.13", "3.14"], "db": ["postgres", "mysql", "sqlite"],
          "batch": [1, 8, 64, 256], "os": ["linux", "macos", "windows"]}
rows = pairwise(matrix)
print(len(rows), "rows instead of", 4 * 3 * 4 * 3)
```

- **依据：** 大多数配置相关的 bug 由一个参数或两个参数的交互触发（比如「Python 3.14 + Windows」），三个以上参数同时作用才出现的 bug 少得多。两两覆盖用很少的用例抓住了大部分。
- **下界：** 用例数至少是最大的两个参数取值数之积：这里 4 × 4 = 16。上面的贪心算法得到 18，专门的工具（如微软的 PICT、Python 的 `allpairspy`）通常更接近下界。
- **约束：** 有些组合根本不存在（某数据库不支持某操作系统），要在生成时排除，否则会生成跑不起来的配置。
- **局限：** 它不保证三个参数一起作用的 bug 被抓住。对高风险的组合（线上最常见的配置、刚改过的代码路径）要额外加上全组合或三三组合；对线上真实流量里占比最高的几套配置，单独固定成必跑项。
- **和分层结合：** 每次提交只跑最常用的 1–2 套配置，夜间跑两两组合的 18 套，发版前对高风险参数做更强的组合。
