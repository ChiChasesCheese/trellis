---
id: tlc-python-dp-space-compression-7-problems
node: python.dp-space-compression
type: qa
step: 7
---
## Q
**DP 降维｜本组题目各用哪一种压缩**

先写二维表之后，本组哪些题可以压成两行、一行原地、背包方向、左上角变量？怎么快速选？

## A
```python
def plan(old_left: bool, new_left: bool) -> str:
    """old_left：要读左边的上一行旧值；new_left：要读左边的本行新值。"""
    if old_left and new_left:
        return "一行 + 变量暂存旧值"
    return "一行，j 倒序" if old_left else "一行，j 正序"

print(plan(False, True), plan(True, False), plan(True, True))   # 一行，j 正序 一行，j 倒序 一行 + 变量暂存旧值
```

- **两行 `prev` / `cur`**（每一行只读上一行）：LC 62 不同路径、LC 64 最小路径和、LC 120 三角形最小路径和、LC 188 买卖股票 IV（行是天数）、LC 787 K 站中转内最便宜的航班（行是航班趟数）。
- **一行原地，正序**（上方旧、左边新）：LC 62、LC 64、LC 97 交错字符串、LC 120。
- **背包方向**：0-1 倒序，LC 416 分割等和子集、LC 1049 最后一块石头的重量 II、LC 494 目标和；完全背包正序，LC 518 零钱兑换 II、LC 322 零钱兑换；LC 887 鸡蛋掉落读上一行的 `j-1`，同 0-1 倒序。
- **左上角要变量**：LC 1143 最长公共子序列、LC 72 编辑距离、LC 221 最大正方形、LC 44 通配符匹配、LC 10 正则表达式匹配。
- **只读左上角，倒序即可**：LC 718 最长重复子数组、LC 115 不同的子序列。
- **不压缩**：LC 5 最长回文子串（区间 DP）；要输出方案的版本。
