---
id: hi-lld-connect-four-6-place-disc
node: lld.problem-breakdowns.connect-four
type: qa
step: 6
---
## Q
**placeDisc：子如何下坠**｜低层设计 · 题目拆解

`placeDisc(column, color)` 怎么让子落到最低的空位？需要处理哪些边界？

## A
```python
def place_disc(self, column: int, color: DiscColor) -> int:
    if column < 0 or column >= self.cols:   # 越界
        return -1
    if not self.can_place(column):          # 满列：顶行已有子
        return -1
    for row in range(self.rows - 1, -1, -1):   # 从底行向上找第一个空格
        if self.grid[row][column] is None:
            self.grid[row][column] = color
            return row
    return -1
```

**要点。** 行 0 在顶部，行 5 在底部，所以从 `rows - 1` 往上找；`canPlace` 只需看顶行 `grid[0][column]` 是否为空，就知道这一列有没有空位。

**为什么。** 返回落点行，后面的 `checkWin` 只检查刚落下的这一子，而不是全盘扫描。

**易错。** 把越界与满列校验放在 Game 里，会让 Game 知道 Board 的内部尺寸，职责就混了。
