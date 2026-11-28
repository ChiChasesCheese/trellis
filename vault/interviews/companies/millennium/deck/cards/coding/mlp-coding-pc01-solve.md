---
id: mlp-coding-pc01-solve
node: coding.pc01
step: 1
type: qa
---
## Q
**百万行分组求和：题与解**｜编程轮

一份有几百万行的 CSV，每行是 `id,amount`（没有表头，金额是十进制字符串，可以为负，代表退款）。按 `id` 求金额总和，输出按 `id` 排序、保留两位小数。数据大到不一定装得进内存时怎么做？

## A
**一句话思路。** 先写单遍 dict 累加（边读边加，内存里只有每个 id 的总额）；被追问装不下时，切块、每块各自聚合，再把局部 dict 合并。因为加法满足结合律（先加哪块都一样），分块结果和一次性算完永远相同。

```python
import csv
from decimal import Decimal, ROUND_HALF_UP

def to_amount(raw):
    # 金额用 Decimal，不用 float：钱不能有浮点误差
    try:
        return Decimal(raw.strip()).quantize(Decimal("0.01"), ROUND_HALF_UP)
    except Exception:
        raise ValueError(f"bad amount {raw!r}")

def group_sum(lines):
    totals = {}
    # csv.reader 是迭代器：一行一行读，不先 readlines() 整份文件
    for fields in csv.reader(ln for ln in lines if ln.strip()):
        if len(fields) != 2 or not fields[0].strip():
            raise ValueError(f"bad row {fields!r}")
        key = fields[0].strip()
        totals[key] = totals.get(key, Decimal("0.00")) + to_amount(fields[1])
    return totals

def chunked_group_sum(lines, chunk_size):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    rows = [ln for ln in lines if ln.strip()]
    result = {}
    for i in range(0, len(rows), chunk_size):
        partial = group_sum(rows[i:i + chunk_size])   # 每块独立聚合
        for key, amt in partial.items():              # 再合并：同一个 id 可能分在多块
            result[key] = result.get(key, Decimal("0.00")) + amt
    return result

lines = ["A,10.50", "B,5.25", "A,3.75", "C,100", "B,0.75"]
for k, v in sorted(chunked_group_sum(lines, 2).items()):
    print(f"{k},{v:.2f}")   # A,14.25  B,6.00  C,100.00
```

**复杂度。** 时间 O(n)，每行常数次操作；空间 O(不同 id 的个数)，与行数无关。分块版每块额外占 O(chunk_size)。

**边写边讲。**
- "Amounts are money, so I'll use **Decimal**, not float, to avoid rounding drift."
- "A **dict keyed by id** gives one pass with O(1) lookups, and I only keep the running totals in memory."
- "Sum is **associative**, so chunking and re-aggregating gives exactly the same answer as one pass, whatever the chunk size."
