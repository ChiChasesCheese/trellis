---
id: lct-learn-list-tree-backtracking-4-2
node: list-tree-backtracking.4.2
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 划分型回溯**｜学习卡

套路是什么？

## A
**一句话。** 切字符串等价于在相邻字符的空隙里放不放逗号，是子集型回溯：`dfs(i)` 表示 `s[i:]` 还没切，枚举这一段的结束位置 `j`，这一段合法就记入 `path` 并递归 `dfs(j + 1)`，回来撤销。

下图：LC 131 切 "aab"；每层枚举当前这一段到哪结束，合法才递归剩下的后缀。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<line x1="137.3" y1="27.9" x2="82.7" y2="62.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="155.6" y1="33.9" x2="164.4" y2="56.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="163.8" y1="25.8" x2="256.2" y2="64.2" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="62.3" y1="82.9" x2="47.7" y2="107.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="79.4" y1="81.7" x2="100.6" y2="108.3" stroke-width="1.2" style="stroke:var(--dim,#6b7280)" stroke-dasharray="4 3"/>
<line x1="40.0" y1="135.0" x2="40.0" y2="150.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="170.0" y1="85.0" x2="170.0" y2="105.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="150" cy="20" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="24" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">aab</text>
<circle cx="70" cy="70" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="70" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="170" cy="70" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">aa</text>
<circle cx="270" cy="70" r="15" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="270" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">aab</text>
<circle cx="40" cy="120" r="15" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="40" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<circle cx="110" cy="120" r="15" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2"/>
<text x="110" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ab</text>
<circle cx="40" cy="165" r="15" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="169" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<circle cx="170" cy="120" r="15" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b</text>
<text x="295" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">✗</text>
<text x="132" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">✗</text>
<text x="64" y="169" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">[a,a,b]</text>
<text x="193" y="124" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">[aa,b]</text>
<text x="230" y="150" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">每层枚举这一段的终点 j</text>
<text x="230" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不是回文就不往下</text>
</svg>

```python
def partition(s):                    # LC 131：每段是回文
    n, ans, path = len(s), [], []
    def dfs(i):                      # 还要切 s[i:]
        if i == n:                   # 字符用完：一种划分
            ans.append(path[:])      # 拷贝
            return
        for j in range(i, n):        # 枚举这一段的结束位置
            t = s[i:j + 1]
            if t == t[::-1]:         # 回文才能当一段
                path.append(t)
                dfs(j + 1)
                path.pop()           # 恢复现场
    dfs(0)
    return ans
```

**要点。**
- 为什么对？：`n - 1` 个空隙放逗号的每个子集恰对应一种划分，搜索树不重不漏；最坏 `O(n · 2^n)`，判回文可先用区间 DP 预处理成 `O(1)`。
- LC 93 怎么改？：恰好 `4` 段，每段至多 `3` 位；`left = 4 - len(path)`，剩余字符数不在 `[left, 3 * left]` 就剪枝；段有前导零（长度大于 `1` 且以 `0` 开头）或 `> 255` 时用 `break`（更长只会更差）；`4` 段且字符恰好用完才收集。
- LC 291 怎么改？：按 `pattern` 的字母逐个决定它对应 `s` 的哪一段；字母已有映射就核对 `startswith`，新字母才枚举子串，并用 `used` 集合保证双射；返回布尔，两边必须同时用完；回溯时 `mp` 和 `used` 一起撤销。

**易错点。**
- LC 93 放行前导零：`"010010"` 应得 `["0.10.0.10","0.100.1.0"]`；凑够 `4` 段就收集而不查字符是否用完，会出现 `"2.5.5.2"`。
- 收集时不拷贝 `path`：`"aab"` 应得 `[["a","a","b"],["aa","b"]]`，不拷贝得到空列表。
- LC 291 不记已占用的子串：`pattern = "ab"`、`s = "aa"` 应为假；终止时只看 `pattern` 用完：`"a"`、`"ab"` 应为假。

**对应题目。** LC 131 分割回文串、LC 93 复原 IP 地址、LC 291 单词规律 II
