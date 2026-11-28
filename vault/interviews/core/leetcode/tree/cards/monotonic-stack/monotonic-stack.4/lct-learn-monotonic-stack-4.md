---
id: lct-learn-monotonic-stack-4
node: monotonic-stack.4
type: qa
step: 1
---
## Q
**单调栈 › 最小字典序**｜学习卡

套路是什么？

## A
**一句话。** 字典序由第一个不同的位置决定，所以让前面的位置尽量小：新字符比栈顶小，且弹掉栈顶后仍能凑出合法答案，就弹；栈就是当前字典序最小的候选。

下图：LC 1673，新数比栈顶小、且弹掉后仍能凑满 `k` 个就弹，栈是当前字典序最小的候选。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<text x="14" y="32" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 3</text>
<rect x="70" y="14" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="31.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="14" y="64" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 5</text>
<rect x="70" y="46" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="63.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="106" y="46" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124.0" y="63.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="14" y="96" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 2</text>
<rect x="70" y="78" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="95.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="128" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读 6</text>
<rect x="70" y="110" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="88.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="106" y="110" width="36" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="124.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="160" y="92" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2 比栈顶小，弹掉后剩下的</text>
<text x="160" y="106" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">还够凑满 k：弹 5、3</text>
<text x="170" y="154" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">nums = [3,5,2,6]，k = 2 → [2, 6]</text>
</svg>

```python
def smallest_subseq(nums, k):       # LC 1673；LC 402
    n, st = len(nums), []
    for i, x in enumerate(nums):
        # 栈顶更大，且弹掉后剩下的还够凑满 k 个：弹
        while st and st[-1] > x and len(st) + n - i > k:
            st.pop()
        if len(st) < k:             # 栈没满才放
            st.append(x)
    return st

def remove_duplicate_letters(s):    # LC 316 / 1081
    last = {c: i for i, c in enumerate(s)}  # 每个字符最后出现的位置
    st = []
    for i, c in enumerate(s):
        if c in st:                 # 已在栈里：保留靠前的
            continue
        while st and st[-1] > c and last[st[-1]] > i:
            st.pop()                # 栈顶后面还会出现：先弹，晚点再放
        st.append(c)
    return "".join(st)
```

**要点。**
- 为什么对？：弹的条件保证“弹掉之后仍然合法”，且换上的更小字符让字典序严格变小；不弹的元素要么更小要么不能丢。
- LC 402 移掉 K 位数字怎么改？：取 `k = n - 删除数` 的最小子序列，`"".join(...).lstrip("0") or "0"`。
- LC 321 拼接最大数怎么改？：枚举分给两个数组的长度，各自求最大的定长子序列（比较反过来），再合并，平局时比较剩余整个后缀。

**易错点。**
- 316 弹出时不检查后面是否还有：`s = "cba"` 应得 `"cba"`，会得到 `"a"`。
- 316 不跳过已在栈里的字符：`s = "aa"` 应得 `"a"`，会得到 `"aa"`。
- 402 不去前导零：`num = "10200"`、`k = 1` 应得 `"200"`；删光 `num = "10"`、`k = 2` 应得 `"0"`。

**对应题目。** LC 321 拼接最大数、LC 1673 找出最具竞争力的子序列、LC 316 去除重复字母、LC 402 移掉 K 位数字、LC 1081 不同字符的最小子序列
