---
id: lct-learn-monotonic-stack-1-2
node: monotonic-stack.1.2
type: qa
step: 1
---
## Q
**单调栈 › 单调栈 › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 进阶题要用到栈的整个生命周期：弹出的那一刻就是结算时机，栈里留下的是满足某种单调性的候选集。

下图：LC 1944，从右往左维护单调栈，被弹出的每个人都是 `i` 能看到的。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="43" y="50" width="38" height="80" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="62.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10</text>
<rect x="87" y="82" width="38" height="48" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="106.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="131" y="66" width="38" height="64" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="175" y="90" width="38" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="194.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="219" y="42" width="38" height="88" rx="3" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="238.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<rect x="263" y="58" width="38" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<text x="62.0" y="42" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<text x="170" y="150" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)"></text>
<text x="185" y="16" text-anchor="start" font-size="10" font-family="sans-serif" fill="currentColor">弹出的 6、8：i 都看得到</text>
<text x="185" y="30" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第一个更高的 11 也看得到</text>
<text x="170" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">弹出那一刻就结算：ans[0] = 2 + 1 = 3</text>
</svg>

```python
def can_see(h):                     # LC 1944（身高互不相同）
    ans, st = [0] * len(h), []
    for i in range(len(h) - 1, -1, -1):
        while st and st[-1] < h[i]:
            st.pop()
            ans[i] += 1             # 弹出的都被 i 看到
        if st:
            ans[i] += 1             # 挡住 i 的第一个更高者也能看到
        st.append(h[i])
    return ans

def max_width_ramp(nums):           # LC 962
    st, ans = [], 0                 # st：左端点候选，严格递减的前缀最小值
    for i, x in enumerate(nums):
        if not st or nums[st[-1]] > x:
            st.append(i)
    for j in range(len(nums) - 1, -1, -1):  # 右端点从大往小
        while st and nums[st[-1]] <= nums[j]:
            ans = max(ans, j - st.pop())    # 弹出即结算
    return ans
```

**要点。**
- 为什么对？：1944 中弹出的都比 `h[i]` 矮，被 `i` 看到；栈里剩下的第一个更高，是最后一个能看到的。962 中只有前缀最小值才可能是最优左端点，倒着扫右端点，每个左端点第一次配到的就是最远的 `j`。
- LC 853 车队怎么改？：按位置从近到远排序，算到达时间 `(target - p) / s`，只有比栈顶更慢的才入栈（否则并入前面的车队），栈大小就是答案。

**易错点。**
- 1944 漏掉挡板那个 `+1`：`[10,6,8,5,11,9]` 应得 `[3,1,2,1,1,0]`，漏了得到 `[2,0,1,0,1,0]`。
- 962 正着扫右端点：`[6,0,8,2,1,5]` 应得 `4`，正着扫会得到 `0`。
- 853 用整数除法算时间：`target = 10`、车 `(8, 2)` 与 `(0, 9)` 应得 `2`，整除后时间都是 `1`，被并成 `1`。

**对应题目。** LC 853 车队、LC 962 最大宽度坡、LC 1944 队列中可以看到的人数
