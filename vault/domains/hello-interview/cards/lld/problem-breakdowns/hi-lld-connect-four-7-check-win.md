---
id: hi-lld-connect-four-7-check-win
node: lld.problem-breakdowns.connect-four
type: qa
step: 7
---
## Q
**checkWin：方向向量统一，而不是四个检查器类**｜低层设计 · 题目拆解

怎样检查刚落下的一子是否让某方连成四子？为什么「每个方向一个 WinChecker 类」是反模式？

## A
```python
DIRS = [(0, 1), (1, 0), (1, 1), (-1, 1)]   # 横、竖、两条斜线

def check_win(self, row: int, col: int, color: DiscColor) -> bool:
    if not self.in_bounds(row, col) or self.grid[row][col] != color:
        return False
    for dr, dc in DIRS:
        # 从落点向两个相反方向数连续同色子，再加上落点本身
        n = 1 + self.count(row, col, dr, dc, color) + self.count(row, col, -dr, -dc, color)
        if n >= 4:
            return True
    return False
```

`count` 沿 `(dr, dc)` 一直走到出界或遇到异色为止。

**为什么。** 四个方向的算法完全相同，差别只是一对数字，应当「参数化」而不是「多态化」。游戏几何固定，永远只有四个方向，建四个类是为不存在的需求预留扩展（YAGNI）；策略模式适合运行时要换实现、或会继续增加实现的场景，比如支付方式。

**取舍。** 若变体改成五子连珠，只改一个常量，而不是动四个类。
