---
id: lct-learn-dp-11-1
node: dp.11.1
type: qa
step: 1
---
## Q
**动态规划 › 优化 DP › 前缀和优化 DP**｜学习卡

套路是什么？

## A
**一句话。** 前缀和优化 DP：转移是一段区间和 `f[i] = Σ f[l..r]` 时，维护前缀和 `s`，每个状态 `O(1)` 而不是 `O(n)`。

下图：LC 1997，`f[i]` 要一段区间的和，用前缀和 `s` 两项相减即得。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="20" y="46" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f0</text>
<rect x="66" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="89.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f1</text>
<rect x="112" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="135.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f2</text>
<rect x="158" y="46" width="46" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="181.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f3</text>
<rect x="204" y="46" width="46" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="227.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f4</text>
<rect x="250" y="46" width="46" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273.0" y="64.0" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">f5</text>
<line x1="66.0" y1="40" x2="66.0" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="204.0" y1="40" x2="204.0" y2="34" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="66.0" y1="40" x2="204.0" y2="40" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="135.0" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Σ f[nv..i-1] = s[i] - s[nv]</text>
<line x1="89.0" y1="92" x2="89.0" y2="78" stroke-width="1.2" stroke="currentColor"/>
<polygon points="89.0,78.0 92.0,84.3 86.0,84.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="89.0" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">nv</text>
<line x1="227.0" y1="92" x2="227.0" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="227.0,78.0 230.0,84.3 224.0,84.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="227.0" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i]</text>
<text x="170" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[i] = 2 + s[i] - s[nv]：区间和 O(1)，整体 O(n)</text>
</svg>

```python
def first_day_all_rooms(next_visit):
    MOD = 10**9 + 7
    n = len(next_visit)
    s = [0] * n                  # s[i] = f[0]+...+f[i-1]
    for i in range(n - 1):
        # f[i]：首次到房间 i 之后，再过几天首次到 i + 1
        # = 1（被送回 nv）+ 重走 nv..i-1 + 1（走到 i+1）
        nv = next_visit[i]
        f = (2 + s[i] - s[nv]) % MOD
        s[i + 1] = (s[i] + f) % MOD
    return s[n - 1]              # 总天数 = f[0] + ... + f[n-2]
```

**要点。**
- 为什么对？：第一次到 `i` 时访问次数是奇数，被送回 `nv`；从 `nv` 重走到 `i` 时，这些房间都是「首次到下一间」的情形，天数恰好是 `f[nv..i-1]` 之和，再走一步到 `i+1`。
- 前缀和优化了什么？：朴素地对每个 `i` 求 `f[nv..i-1]` 要 `O(n)`，总 `O(n^2)`；用 `s[i] - s[nv]` 变成 `O(1)`。
- 什么时候想到这个套路？：转移方程里出现「某个下标范围内所有状态之和」，就把和维护成前缀和（或滑窗和）。

**易错点。**
- 漏减 `s[nv]`，写成 `2 + s[i]`：`[0,1,2,0]` 得 `14`，应为 `6`。
- 答案取 `s[n]`：下标越界，应为 `s[n - 1]`，到最后一间那天就访问完了。
- 取模后的差为负：Python 的 `%` 安全；C++ / Java 要写 `(… + MOD) % MOD`。

**对应题目。** LC 1997 访问完所有房间的第一天
