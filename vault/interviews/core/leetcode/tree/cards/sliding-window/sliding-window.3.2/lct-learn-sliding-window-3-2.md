---
id: lct-learn-sliding-window-3-2
node: sliding-window.3.2
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 单序列双指针 › 相向双指针**｜学习卡

套路是什么？

## A
**一句话。** 两个指针从两端向中间走，每步比较后能确定一端不可能再出现在答案里，把它扔掉；每步扔一个，`O(n)`。

下图：数组已排序，每次比较都能扔掉一端，所以两指针合计走 `n` 步。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<rect x="20" y="46" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="45.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-4</text>
<rect x="70" y="46" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="95.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">-1</text>
<rect x="120" y="46" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="170" y="46" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="195.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="220" y="46" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="270" y="46" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="295.0" y="64.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<line x1="45.0" y1="30" x2="45.0" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="45.0,44.0 42.0,37.7 48.0,37.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="45.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k 固定</text>
<line x1="95.0" y1="30" x2="95.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="95.0,44.0 92.0,37.7 98.0,37.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="95.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="295.0" y1="30" x2="295.0" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="295.0,44.0 292.0,37.7 298.0,37.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="295.0" y="26" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<text x="170" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">s = nums[k] + nums[i] + nums[j]</text>
<text x="170" y="124" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s &lt; 0：nums[i] 配谁都太小 → i += 1</text>
<text x="170" y="142" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">s &gt; 0：nums[j] 配谁都太大 → j -= 1</text>
<text x="170" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">s = 0：记答案，跳过重复值，两边都走</text>
</svg>

```python
def three_sum(nums):                # LC 15；LC 167 是内层循环
    nums.sort()
    ans = []
    for k in range(len(nums) - 2):
        if k and nums[k] == nums[k - 1]:
            continue                # 固定数去重
        i, j = k + 1, len(nums) - 1
        while i < j:
            s = nums[k] + nums[i] + nums[j]
            if s < 0:
                i += 1              # nums[i] 配谁都太小
            elif s > 0:
                j -= 1              # nums[j] 配谁都太大
            else:
                ans.append([nums[k], nums[i], nums[j]])
                i += 1
                while i < j and nums[i] == nums[i - 1]:
                    i += 1          # 跳过重复的 nums[i]
                j -= 1
    return ans
```

**要点。**
- 为什么对？：和太小说明 `nums[i]` 与剩下的任何数都配不够，排除 `i`；和太大排除 `j`；每步排除一个，不会漏解。
- LC 11 盛最多水的容器、LC 42 接雨水怎么改？：11 只移动较短的板（长板留着才可能更大）；42 结算较矮的一侧，水位由已扫的一侧最高墙决定。
- LC 259 较小的三数之和、LC 1099 怎么改？：和小于 `target` 时 `[i+1..j]` 全满足，一次加 `j - i`，再 `i += 1`；1099 记录小于 `k` 的最大和，没有则 `-1`。
- LC 977 有序数组的平方怎么改？：比较两端的平方，较大者从结果末尾往前填。

**易错点。**
- 命中后不跳重复值：`nums = [-2,0,0,2,2]` 应只得 `[[-2,0,2]]`。
- 固定数和后一个比较去重：`nums = [-1,-1,2]` 应得 `[[-1,-1,2]]`，要和前一个比较。
- 259 命中只加 `1`：`nums = [-2,0,1,3]`、`target = 2` 应得 `2`，要加 `j - i`。

**对应题目。** LC 16 最接近的三数之和、LC 259 较小的三数之和、LC 15 三数之和、LC 18 四数之和、LC 11 盛最多水的容器、LC 2422 使用合并操作将数组转换为回文序列、LC 977 有序数组的平方、LC 42 接雨水、LC 167 两数之和 II - 输入有序数组、LC 1099 小于 K 的两数之和、LC 125 验证回文串
