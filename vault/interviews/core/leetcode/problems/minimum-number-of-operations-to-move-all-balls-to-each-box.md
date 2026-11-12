---
slug: minimum-number-of-operations-to-move-all-balls-to-each-box
---
## Q
**LC 1769 移动所有球到每个盒子所需的最小操作数**｜Medium

`boxes` 是 0/1 字符串，`1` 表示盒子里有球，一步把一个球移到相邻盒子。对每个 `i` 求把所有球移到盒子 `i` 的最少步数。

## A
**一句话。** 答案是各球到 `i` 的距离和，`i→i+1` 时左边球各远 1、右边球各近 1，一遍递推。

```python
def min_operations(boxes):
    right = boxes.count("1")     # 右边的球数
    left = 0                     # 左边（含当前）的球数
    cur = sum(j for j, b in enumerate(boxes) if b == "1")
    ans = []
    for b in boxes:
        ans.append(cur)
        if b == "1":             # 先把当前球算进左边
            left += 1
            right -= 1
        cur += left - right
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- `cur += left - right` 放在球数更新前：`"110"` 得 `[1,-1,-1]`，应为 `[1,1,3]`。
- 先改 `cur` 再 `append`：答案整体错位。

**追问。**
- 只要最小的那个答案？：最优位置是球位置的中位数。
- 球有权重呢？：球数换成权重和，递推不变。

**同模式。** LC 2602 使数组元素全部相等的最少操作次数、LC 1685 有序数组中差绝对值之和、LC 296 最佳的碰头地点、LC 834 树中距离之和
