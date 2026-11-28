---
id: lct-learn-list-tree-backtracking-4-3
node: list-tree-backtracking.4.3
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 组合型回溯**｜学习卡

套路是什么？

## A
**一句话。** 组合型回溯是带个数约束的子集型：一层选一个元素、只往一个方向选保证集合不重复，并用「还差 `d` 个而可选元素不足 `d` 个」剪掉死枝，剪完每个分支都至少通向一个答案。

下图：LC 77（n = 4，k = 2）的搜索树；「还差 `d` 个却不足 `d` 个可选」的分支直接不进。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<line x1="138.7" y1="26.5" x2="71.3" y2="65.5" stroke-width="1.2" stroke="currentColor"/>
<line x1="150.0" y1="33.0" x2="150.0" y2="59.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="160.9" y1="27.1" x2="219.1" y2="64.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="162.3" y1="24.3" x2="287.7" y2="67.7" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="52.7" y1="82.8" x2="32.3" y2="113.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="60.0" y1="85.0" x2="60.0" y2="111.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="67.3" y1="82.8" x2="87.7" y2="113.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="146.4" y1="84.5" x2="138.6" y2="111.5" stroke-width="1.2" stroke="currentColor"/>
<line x1="154.7" y1="84.1" x2="165.3" y2="111.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="230.0" y1="85.0" x2="230.0" y2="111.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="150" cy="20" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="24" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">n=4</text>
<circle cx="60" cy="72" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="60" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="150" cy="72" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="230" cy="72" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="230" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="300" cy="72" r="13" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="300" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<circle cx="25" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="25" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="60" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="60" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<circle cx="95" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<circle cx="135" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="135" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<circle cx="170" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<circle cx="230" cy="124" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="230" y="128" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="300" y="102" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">剪掉：</text>
<text x="300" y="116" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">还差 2 个</text>
<text x="300" y="130" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只剩 1 个</text>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k = 2：j 从 i 降到 d，只选更小的；第二层每个节点都是答案</text>
</svg>

```python
def combine(n, k):                   # LC 77
    ans, path = [], []
    def dfs(i):                      # 可选元素是 1..i
        d = k - len(path)            # 还要选 d 个
        if d == 0:
            ans.append(path[:])      # 拷贝
            return
        for j in range(i, d - 1, -1):    # j < d 时凑不够，不进
            path.append(j)
            dfs(j - 1)               # 只选更小的：集合不重复
            path.pop()               # 恢复现场
    dfs(n)
    return ans
```

**要点。**
- 为什么下界是 `d`？：选了 `j` 后候选是 `1..j-1`、还差 `d-1` 个，需要 `j - 1 >= d - 1`，即 `j >= d`；这既必要又充分，所以没有死枝，时间 `O(k · C(n, k))`。
- 为什么不重复？：下一个必须比刚选的小，每个集合只有从大到小这一种选取序列，对应唯一的叶子。
- LC 22 怎么改？：个数约束换成合法性约束，`dfs(s, left, right)` 填一位：`left < n` 可放 `(`，`right < left` 可放 `)`，`left == right == n` 收集；这两条恰是有效括号串的充要条件，叶子数是卡特兰数。

**易错点。**
- 下界写成 `1`：答案对但死枝全留着，`n = 20`、`k = 10` 展开 `616666` 个节点，加 `j >= d` 只要 `352716` 个。
- 下界多剪一个（`j >= d + 1`）：`n = 4`、`k = 2` 应得 `6` 个，会丢掉以 `1` 结尾的三个。
- LC 22 右括号条件写成「右括号数 < `n`」：`n = 2` 会生成 `")(()"`，应只有 `["(())","()()"]`。

**对应题目。** LC 77 组合、LC 22 括号生成
