---
id: lct-learn-dp-11-3
node: dp.11.3
type: qa
step: 1
---
## Q
**动态规划 › 优化 DP › 单调队列优化 DP**｜学习卡

套路是什么？

## A
**一句话。** 切成「段和非递减」的最多段：`f[i]` 随分割点 `j` 单调不降，取最右的可行 `j`，可行条件 `s[j] + last[j] <= s[i]` 的左侧值递增，用单调队列做到线性。

下图：队首是最右的可行分割点；新的 `i` 更靠右且门槛更低时，队尾旧点永远用不上。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 225">
<rect x="66.2" y="7.5" width="207.5" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新的 i，q 里的 key(j) 严格递增</text>
<rect x="48.8" y="55.5" width="242.3" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="72.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">次队首也可行（key ≤ s[i]）：popleft</text>
<rect x="76.0" y="96.0" width="188.1" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="112.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j = q[0]：f[i] = f[j] + 1</text>
<text x="170" y="127.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">last[i] = s[i] - s[j]</text>
<rect x="88.3" y="153.5" width="163.4" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="170.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">队尾 key ≥ key(i)：pop</text>
<rect x="134.2" y="195.5" width="71.7" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="212.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">append i</text>
<path d="M 170.0 32.5 L 170.0 55.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,55.5 167.0,49.2 173.0,49.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 80.5 L 170.0 96.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,96.0 167.0,89.7 173.0,89.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 136.0 L 170.0 153.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,153.5 167.0,147.2 173.0,147.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 178.5 L 170.0 195.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,195.5 167.0,189.2 173.0,189.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def find_maximum_length(nums):
    n = len(nums)
    s = [0] * (n + 1)                # 前缀和
    for i, x in enumerate(nums):
        s[i + 1] = s[i] + x
    f = [0] * (n + 1)                # f[i]：前 i 个数最多切几段
    last = [0] * (n + 1)             # 取到 f[i] 时最后一段的和
    key = lambda j: s[j] + last[j]   # j 作末段起点的可行门槛
    q = deque([0])                   # key 严格递增
    for i in range(1, n + 1):
        while len(q) > 1 and key(q[1]) <= s[i]:
            q.popleft()              # 次队首也可行：队首不是最右
        j = q[0]
        f[i] = f[j] + 1
        last[i] = s[i] - s[j]
        while q and key(q[-1]) >= key(i):
            q.pop()                  # i 更靠右且 key 更小，旧的无用
        q.append(i)
    return f[n]
```

**要点。**
- 为什么对？：段数随 `j` 单调不降，且越靠右最后一段和越小，对后面越有利，所以只要最右的可行 `j`；可行的 `j` 的 key 递增，队首弹到次队首不可行为止。
- 滑动窗口取最优 `dp`（LC 1696）怎么改？：队首下标过期就弹出，`dp[i] = nums[i] + dp[队首]`，再按 `dp` 值从队尾弹小的。

**易错点。**
- 取最左的可行 `j`：段数偏少，`[1,2,3,4]` 得 `1`，应为 `4`。
- 条件写成 `<`：非递减允许相等，`[3,3]` 得 `1`，应为 `2`。
- 队首只弹一次：要用 `while` 弹到次队首不可行为止。

**对应题目。** LC 2945 找出最长非递减数组的长度
