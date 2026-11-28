---
id: lct-learn-monotonic-stack-1-1
node: monotonic-stack.1.1
type: qa
step: 1
---
## Q
**单调栈 › 单调栈 › 基础**｜学习卡

套路是什么？

## A
**一句话。** 找每个元素右边（左边）第一个更大的数：栈里存还可能成为别人答案的候选，新元素先弹掉被它挡住的，每个元素进出各一次，`O(n)`。

下图：LC 739，从右往左扫；栈里是还可能成为别人答案的候选，栈底到栈顶递减。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="23" y="58" width="31" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="60" y="50" width="31" height="80" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="97" y="42" width="31" height="88" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<rect x="134" y="74" width="31" height="56" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="171" y="90" width="31" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="208" y="66" width="31" height="64" rx="3" fill="none" style="stroke:var(--dim,#6b7280)" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="245" y="34" width="31" height="96" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<rect x="282" y="58" width="31" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">73</text>
<text x="75.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">74</text>
<text x="112.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">75</text>
<text x="149.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">71</text>
<text x="186.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">69</text>
<text x="223.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">72</text>
<text x="260.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">76</text>
<text x="297.5" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">73</text>
<line x1="112.5" y1="34" x2="112.5" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="112.5,48.0 109.5,41.7 115.5,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="112.5" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<path d="M 112.5 48 Q 186.5 20 260.5 40" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="260.5,40.0 254.1,37.1 258.7,33.2" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="168" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">从右往左：弹掉 ≤ 75 的 71、72（虚框），栈顶 76 就是答案</text>
</svg>

```python
def right_greater(nums):            # LC 739：答案 right[i] - i
    n = len(nums)
    right = [n] * n                 # 没有则为 n
    st = []                         # 下标；值从栈底到栈顶递减
    for i in range(n - 1, -1, -1):
        while st and nums[st[-1]] <= nums[i]:
            st.pop()                # 被 i 挡住，不会再是别人的答案
        if st:
            right[i] = st[-1]       # 栈顶就是右边最近的更大者
        st.append(i)
    return right
```

**要点。**
- 为什么对？：被弹出的元素比 `nums[i]` 小且更靠右，对 `i` 左边的任何元素来说，`i` 总是比它更近更大，所以它永远不会是答案。
- LC 496、LC 503 怎么改？：496 对 `nums2` 全体做一遍，存成 `{值: 下一个更大值}` 再查询；503 环形数组扫两圈，下标取模，只记录第一圈的答案。
- 左边第一个更大怎么写？：从左往右扫，同样的弹出，弹完后栈顶就是左边第一个更大；求更小则把比较反过来。

**易错点。**
- 弹出条件的严格性：LC 739 `[70,70]` 应得 `[0,0]`，弹出写成 `<` 会得到 `[1,0]`。
- 栈里存值却要距离：`[73,74]` 只拿到 `74`，求不出相隔 `1` 天，需要距离就存下标。
- 503 只扫一圈：`[1,2,1]` 应得 `[2,-1,2]`，一圈得到 `[2,-1,-1]`。

**对应题目。** LC 739 每日温度、LC 496 下一个更大元素 I、LC 503 下一个更大元素 II
