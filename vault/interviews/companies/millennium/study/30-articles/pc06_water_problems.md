# pc06 · Water Problems：练的是"双指针收缩的正确性证明"

> [!tldr]
> - 这题考的是：能不能讲清楚"为什么每步移动较矮/较小的那一侧不会漏掉最优解"
> - 三步套路：先写出暴力 O(n²)/O(n) 想法 → 找到"移动谁"的判据 → 把判据讲成交换论证
> - 最值得带走的一个模式：**双指针收缩类问题，正确性不是靠试出来的，是靠"移动另一侧不可能更优"的论证**

## 1. 题目在说什么（人话版）

Part 1（LC 11）：一排竖线，选两条围成的"容器"能装多少水，取最大值。Part 2（LC 42）：同一排竖线本身就是柱子，每根柱子头上能积多少水，求总和。Part 3（reconstructed，LC 407）：把"一排柱子"换成"一整块地形"，求整块地能积多少水。

```
heights = [0,1,0,2,1,0,1,3,2,1,2,1]
下标7（高度3）左边最高是2，右边最高也是3 → 它自己头上积不了水
下标2（高度0）左边最高是1，右边最高是2 → 头上能积 min(1,2)-0 = 1
… 全部加起来 = 6
```

## 2. 读题：把文字变成模型

- **实体**：Part 1/2 是一维数组 `heights`；Part 3 是二维网格 `grid`。
- **Part 1 的问题**：选两条边界，装水量由**较矮**的那条决定。
- **Part 2 的问题**：每根柱子头上的水由**左右两边最高柱子中较矮的那个**减去自己决定。
- **Part 3 的问题**：每个格子头上的水由"从边界不下坡也能摸到它的最低那圈围墙"决定——这是 Part 2 "左右两个方向的最矮上限" 在二维里的推广："所有方向里最矮的那圈上限"。
- **一句话建模**：三道题都是"某种边界/上限决定了能积多少水"，只是维度和"上限"的计算方式不同。

> [!note] 为什么选双指针 / 最小堆
> Part 1/2 的暴力解都要对每个位置往两边扫一次（O(n²) 或预处理两个数组 O(n) 空间）；双指针把"两边扫"压成"一边收缩一边确定"，省掉额外数组。Part 3 没法用双指针（二维没有"两端"），但"谁的上限最低就先处理谁"的思想是一样的，换成最小堆。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：`main()` 读入 → 解析 `heights`（或 Part 3 的 `grid`）→ 调 `part1` → 打印。
2. **Part 1 最小可用**：双指针 `l, r` 从两端出发，`best = max(best, min(heights[l], heights[r]) * (r - l))`，移动较矮的一侧。立刻用样例自测（应为 49）。
3. **Part 2 先给 O(n) 空间版**：`left_max[i]`、`right_max[i]` 两个数组，逐格套公式——这版最容易在压力下推出来，先写它拿到分。
4. **被追问 O(1) 空间时**：换成双指针 + 两个 running max（`left_max`、`right_max` 变成两个标量），谁小移动谁。
5. **Part 3**：从"两个方向的上限"换成"最小堆维护当前所有已知边界里最低的那个"，从网格边界开始扩张。
6. **收尾**：输入校验（非负、矩形网格）、少于 2/3 个元素或网格小于 3×3 的空结果。

## 4. 代码怎么组织

```
max_container_area(heights)          # Part 1：双指针
trap_prefix_suffix(heights)          # Part 2 基础版：O(n) 空间
trap_two_pointer(heights)            # Part 2 追问版：O(1) 空间
trap_2d(grid)                        # Part 3：最小堆扩张
_check_heights / _check_grid          # 输入校验集中一处
part1..part3 / main
```

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def max_container_area(heights):
    l, r, best = 0, len(heights) - 1, 0
    while l < r:
        best = max(best, min(heights[l], heights[r]) * (r - l))
        if heights[l] <= heights[r]:
            l += 1          # 矮的一侧限制了面积，只有移动它才可能变好
        else:
            r -= 1
    return best

def trap_two_pointer(heights):
    l, r, left_max, right_max, water = 0, len(heights) - 1, 0, 0, 0
    while l < r:
        if heights[l] <= heights[r]:
            left_max = max(left_max, heights[l])
            water += left_max - heights[l]   # 另一侧必有不矮于 left_max 的柱子担保
            l += 1
        else:
            right_max = max(right_max, heights[r])
            water += right_max - heights[r]
            r -= 1
    return water
```

## 6. Talking through it in the interview

- Before starting: "For the container problem, the area is capped by the shorter wall, so I'll move the shorter pointer inward — moving the taller one can only keep the area the same or shrink it."
- Writing the trapping-rain-water follow-up: "Instead of precomputing left_max and right_max arrays, I'll track two running maxima as the pointers close in, and always resolve the side whose running max is smaller — the other side is guaranteed to have a wall at least that tall somewhere between the two pointers."
- Writing Part 3: "This is the 2D version — no more 'two ends', so I use a min-heap seeded with the border cells and always expand from the lowest known boundary first."
- On delivery: "The worked examples pass; the container and trapping-rain-water answers agree between the two implementations, and the 2D version handles the flat-grid and too-small-grid edge cases."

## 7. 常见跑偏（方法层面，3 条）

- Part 1 移动条件写反（移动较高的一侧）——面积只会变小或不变，一定要先讲清楚"移动矮的一侧才可能变好"再动手写。
- Part 2 直接把 Part 1 的双指针条件抄过来："谁矮移动谁"和"谁的 running max 小移动谁"含义不同，混着讲会把两题的正确性证明搞反。
- Part 3 想用双指针硬套二维——二维没有"两端"，正确的推广方向是"谁的已知边界最低就先扩张谁"（最小堆），不是简单套用一维模板。

## 8. 同族题 / 延伸

- Part 1 → Part 2 → Part 3 本身就是同一族题从一维到二维的递进，练习时建议连着做完整套。
- 练习命令：`python3 loop/mock.py start pc06`
