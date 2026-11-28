---
id: lct-learn-dp-1-2
node: dp.1.2
type: qa
step: 1
---
## Q
**动态规划 › 入门 DP › 打家劫舍**｜学习卡

套路是什么？

## A
**一句话。** 相邻互斥的选取：每个位置偷或不偷，只依赖前两个状态，用两个变量滚动；环和值域类问题都先转成一条直线。

下图：每间房只有两个状态，新状态只依赖上一间的两个状态。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 165">
<rect x="35.0" y="40.0" width="90" height="40" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="80" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">skip</text>
<text x="80" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">这间不偷</text>
<rect x="215.0" y="40.0" width="90" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="260" y="56.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">take</text>
<text x="260" y="71.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">这间偷</text>
<path d="M 125 50 L 215 50" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="215.0,50.0 208.7,53.0 208.7,47.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="42" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">skip + x</text>
<path d="M 215 72 L 125 72" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="125.0,72.0 131.3,69.0 131.3,75.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">max(skip, take)</text>
<path d="M 60 39 C 40 5, 100 5, 90 37" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,37.0 87.9,30.3 93.9,31.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="130" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不偷 → 不偷</text>
<text x="260" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">偷完下一间必须不偷</text>
<text x="170" y="140" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">环形：拆成 nums[:-1]、nums[1:] 两条直线</text>
<text x="170" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">值域（LC 740）：把数值当房子，先聚合 gain</text>
</svg>

```python
def rob(nums):                   # 相邻两间不能同偷
    skip = take = 0              # 不偷 / 偷到当前这间的最优
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)

def rob_circle(nums):            # 首尾相邻：拆成两条直线
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[:-1]), rob(nums[1:]))

def delete_and_earn(nums):       # 数值当房子，x 与 x±1 互斥
    gain = [0] * (max(nums) + 1)
    for x in nums:
        gain[x] += x             # 选了 x 就拿走所有 x
    return rob(gain)
```

**要点。**
- 为什么对？：偷第 `i` 间就不能偷第 `i-1` 间，所以 `take` 只能从上一轮的 `skip` 转来；两个状态必须同时更新。
- LC 213 怎么改？：首尾相邻、不会同时偷：「不偷最后一间」和「不偷第一间」各做一遍直线取大；只有一间要特判。
- LC 740 怎么改？：选了数值 `x` 就删掉 `x±1`，把数值当房子排成一行，房子 `x` 的钱是 `x` 乘出现次数，转成直线打家劫舍。

**易错点。**
- 两个状态分两句更新：`take` 用到了新的 `skip`，等于允许连续偷，`[1,2,3,1]` 得 `7`，应为 `4`。
- LC 213 漏掉单间：`[5]` 两条直线都为空，得 `0`，应为 `5`。
- LC 740 收益只算 `x`：`[2,2,3,3,3,4]` 得 `6`，应为 `9`，要乘出现次数。

**对应题目。** LC 198 打家劫舍、LC 213 打家劫舍 II、LC 740 删除并获得点数
