---
slug: queens-that-can-attack-the-king
---
## Q
**LC 1222 可以攻击国王的皇后**｜Medium

`8 × 8` 棋盘上有若干黑皇后和一个白国王。皇后可沿八个方向（横、竖、斜）直走，但不能越过别的皇后。返回所有能直接攻击到国王的皇后坐标，顺序任意。

## A
**一句话。** 从国王出发向八个方向各走一遍，每个方向遇到的第一个皇后就是能攻击的。

```python
def queens_attack_the_king(queens, king):
    qs = {(x, y) for x, y in queens}
    ans = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == dy == 0:
                continue
            x, y = king[0] + dx, king[1] + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if (x, y) in qs:     # 每个方向的第一个皇后
                    ans.append([x, y])
                    break
                x += dx
                y += dy
    return ans
```

**复杂度。** 时间 `O(1)`（`8 × 8` 固定），空间 `O(q)`。

**易错点。**
- 从皇后出发判断能否到国王：要判断路径上有没有别的皇后，反过来从国王向外走找第一个皇后更简单。
- 找到后不 `break`：同一方向后面的皇后被前一个挡住，不能攻击。
- 方向漏了斜线：八个方向，`dx`、`dy` 各取 `-1, 0, 1` 去掉 `(0, 0)`。

**追问。**
- 这类「方向 + 走到第一个障碍」题还有哪些？：LC 999 可以被一步捕获的棋子数、LC 1958 检查操作是否合法。

**同模式。** LC 999 可以被一步捕获的棋子数、LC 1958 检查操作是否合法、LC 51 N 皇后
