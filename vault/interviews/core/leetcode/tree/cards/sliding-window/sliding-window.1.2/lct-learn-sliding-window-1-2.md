---
id: lct-learn-sliding-window-1-2
node: sliding-window.1.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 定长滑动窗口 › 进阶（选做）**｜学习卡

套路是什么？

## A
**一句话。** 定长窗口里维护的是多重集：用“缺口表 + 仍有缺口的种数 `less`”把“窗口是排列”压成 `O(1)` 可更新的量。

下图：LC 438，pat = "abc"；缺口表只看「还有几种没补满」，整个排列判定变成 `less == 0`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="14" y="38" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">seq</text>
<rect x="50" y="20" width="38" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="69.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="88" y="20" width="38" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="107.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="126" y="20" width="38" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="145.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="164" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="183.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<rect x="202" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="221.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="240" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="259.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="278" y="20" width="38" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="38.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="50" y1="56" x2="50" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="164" y1="56" x2="164" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="50" y1="56" x2="164" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="107.0" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">窗口 k = 3，left = 0</text>
<text x="14" y="106" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">cnt</text>
<rect x="50" y="90" width="54" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="77" y="107" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a: 0</text>
<rect x="104" y="90" width="54" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="131" y="107" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b: 0</text>
<rect x="158" y="90" width="54" height="26" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185" y="107" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c: 0</text>
<text x="222" y="107" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">less = 0</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">入：cnt[c] -= 1，恰好变 0 → less -= 1</text>
<text x="170" y="156" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">出：cnt[out] 原来是 0 → less += 1，再 +1</text>
<text x="170" y="172" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">less == 0 且长度为 k：记下 left</text>
</svg>

```python
def anagram_starts(seq, pat):       # LC 438；LC 567 取第一个
    k = len(pat)
    cnt = Counter(pat)              # cnt[c] > 0：窗口里 c 还缺这么多
    less = len(cnt)                 # 仍有缺口的种类数
    ans = []
    for i, c in enumerate(seq):
        cnt[c] -= 1                 # 入：不在 pat 里则变负
        if cnt[c] == 0:
            less -= 1               # 这种元素恰好补满
        left = i - k + 1
        if left < 0:
            continue
        if less == 0:               # 无缺口且长度为 k：必是排列
            ans.append(left)
        out = seq[left]             # 出：先判断再修改
        if cnt[out] == 0:
            less += 1
        cnt[out] += 1
    return ans
```

**要点。**
- 为什么对？：窗口长度恰为 `len(pat)`，没有任何缺口就不可能有多余，所以只看“缺”。
- LC 30 串联所有单词的子串怎么改？：把词当字母，对 `w` 个偏移各切一遍词序列，再套这个模板，窗口下标换回 `off + w * i`。
- LC 2134 环形交换怎么改？：窗口长为 `1` 的总数 `k`，右端点绕环，答案是 `k` − 窗口内 `1` 的最多个数。
- LC 3652 怎么改？：窗口是被改写的 `k` 个位置，用前缀和 `O(1)` 取窗口增益，答案 = 基础利润 + max(0, 最大增益)。

**易错点。**
- 出窗口先加后判：`s = "abab"`、`p = "ab"` 应得 `[0,1,2]`，先 `cnt[out] += 1` 会只得 `[0]`。
- 入窗口用 `<= 0` 判补满：`s = "aab"`、`p = "ab"` 应得 `[1]`，会得到 `[0]`。
- 2134 全是 `0`：`k = 0`，窗口为空，直接返回 `0`。

**对应题目。** LC 3652 按策略买卖股票的最佳时机、LC 438 找到字符串中所有字母异位词、LC 2134 最少交换次数来组合所有的 1 II、LC 567 字符串的排列、LC 30 串联所有单词的子串
