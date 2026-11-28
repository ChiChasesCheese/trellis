---
id: lct-learn-sliding-window-3-5
node: sliding-window.3.5
type: qa
step: 1
---
## Q
**滑动窗口与双指针 › 单序列双指针 › 原地修改**｜学习卡

套路是什么？

## A
**一句话。** 读指针顺序扫原数组，写指针指向结果区的下一格：该留的元素写到 `nums[w]` 并 `w += 1`；读指针不慢于写指针，所以不会覆盖未读的数。

下图：LC 80（k = 2）；读指针扫原数组，写指针指向结果区的下一格。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 160">
<rect x="20" y="50" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="41.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="62" y="50" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="83.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="104" y="50" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="125.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="146" y="50" width="42" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="167.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="188" y="50" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="209.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="230" y="50" width="42" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="251.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<rect x="272" y="50" width="42" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="293.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="20" y1="44" x2="20" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="188" y1="44" x2="188" y2="38" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="20" y1="44" x2="188" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="104.0" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">结果区 nums[:w]</text>
<line x1="209.0" y1="96" x2="209.0" y2="82" stroke-width="1.2" stroke="currentColor"/>
<polygon points="209.0,82.0 212.0,88.3 206.0,88.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="209.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">w</text>
<line x1="251.0" y1="96" x2="251.0" y2="82" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="251.0,82.0 254.0,88.3 248.0,88.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="251.0" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">读 x</text>
<text x="170" y="136" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">读到 x，与结果区倒数第 k 个比：x ≠ nums[w - k] 才写</text>
<text x="170" y="154" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读指针永远不慢于写指针，不会覆盖未读的数</text>
</svg>

```python
def keep_at_most(nums, k):          # LC 26 k=1，LC 80 k=2
    w = 0                           # nums[:w] 是结果
    for x in nums:
        if w < k or x != nums[w - k]:   # 和结果区倒数第 k 个比
            nums[w] = x
            w += 1
    return w


def sort_colors(nums):              # LC 75，值只有 0/1/2
    p0 = p1 = 0                     # [:p0] 是 0，[p0:p1] 是 1
    for i, x in enumerate(nums):
        nums[i] = 2                 # 先写 2，再用 1、0 覆盖
        if x <= 1:
            nums[p1] = 1
            p1 += 1
        if x == 0:
            nums[p0] = 0
            p0 += 1
```

**要点。**
- 为什么对？：每步 `nums[:w]` 就是已读部分的结果；`w <= i`，写入位置永远不超过读位置。
- LC 283 移动零、LC 27 移除元素怎么改？：留下的条件换成 `x != 0` / `x != val`，写完后 283 把 `nums[w:]` 补零。
- LC 41 缺失的第一个正数怎么改？：数组当哈希表，值 `x` 换到下标 `x-1`，再找第一个 `nums[i] != i + 1` 的位置。
- LC 442 数组中重复的数据怎么改？：访问到 `x` 就把 `nums[|x|-1]` 变负当“见过”记号，再遇到负的就是重复。

**易错点。**
- 80 和原数组 `nums[i-2]` 比较：`nums = [1,1,1,2,2,3]` 应得长度 `5`，要和结果区 `nums[w-k]` 比。
- 75 三次写入顺序错：`nums = [0,1]` 应得 `[0,1]`，必须先写 `2`，再 `1`，最后 `0`。
- 41 用元组交换 `nums[i], nums[nums[i]-1] = ...`：`nums = [3,4,-1,1]` 会出错，先存 `j = nums[i] - 1`，并要求 `nums[j] != nums[i]`。

**对应题目。** LC 442 数组中重复的数据、LC 41 缺失的第一个正数、LC 283 移动零、LC 80 删除有序数组中的重复项 II、LC 26 删除有序数组中的重复项（Remove Duplicates from Sorted Array）、LC 27 移除元素、LC 905 按奇偶排序数组、LC 75 颜色分类
