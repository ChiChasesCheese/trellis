---
id: lct-learn-greedy-5-1
node: greedy.5.1
type: qa
step: 1
---
## Q
**贪心算法 › 思维题 › 从特殊到一般**｜学习卡

套路是什么？

## A
**一句话。** 先考虑特殊情形（全去 `b` 市），再看每个人改去 `a` 市要多花多少（`a - b`），按差值排序取最小的 `n` 个。

下图：LC 1029，从「全去 b」这个特殊情形出发，换人去 a 的代价就是 `a - b`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 130">
<text x="170" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">先设全去 b，再看改去 a 多花多少：a - b</text>
<rect x="50" y="40" width="60" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="80.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">-170</text>
<rect x="110" y="40" width="60" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="140.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">-10</text>
<rect x="170" y="40" width="60" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="200.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="230" y="40" width="60" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="260.0" y="58.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">350</text>
<line x1="50" y1="74" x2="50" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="170" y1="74" x2="170" y2="80" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="50" y1="74" x2="170" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="110.0" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">最小的 n 个去 a</text>
<line x1="170" y1="74" x2="170" y2="80" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="290" y1="74" x2="290" y2="80" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<line x1="170" y1="74" x2="290" y2="74" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="230.0" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">其余去 b</text>
<text x="170" y="120" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">按 a - b 排序，前 n 个去 a 最省</text>
</svg>

```python
def two_city_sched_cost(costs):
    n = len(costs) // 2
    costs.sort(key=lambda c: c[0] - c[1])   # 越小越适合去 a
    return (sum(a for a, _ in costs[:n])
            + sum(b for _, b in costs[n:]))
```

**要点。**
- 为什么对？：先假设所有人去 `b`，改去 `a` 的额外成本是 `a - b`，恰要选 `n` 个人改，当然选额外成本最小的。
- LC 517 怎么改？：总数不能整除 `n` 返回 `-1`；扫描时累加 `surplus = 本台 - 平均`，答案取所有 `max(|前缀和|, surplus)` 的最大值。

**易错点。**
- 只按 `a` 排序：忽略 `b` 的代价，`[[5,10],[1,6],[2,2],[5,6]]` 得 `19`，应为 `14`。
- LC 517 只看 `|前缀和|`：`[0,3,0]` 得 `1`，应为 `2`，中间那台一步只能送出 `1` 件。

**对应题目。** LC 517 超级洗衣机、LC 1029 两地调度
