---
slug: champagne-tower
---
## Q
**LC 799 香槟塔**｜Medium

香槟塔第 `r` 层有 `r + 1` 个杯子，容量 1 杯；顶杯倒入 `poured` 杯，溢出的部分平分流向下一层左右两杯。返回第 `query_row` 行第 `query_glass` 个杯子的盛满比例。

## A
**一句话。** 逐行模拟流经量，每杯把超出 1 的部分平分给下一行左右两杯，答案取 `min(1, 流经量)`。

```python
def champagne_tower(poured, query_row, query_glass):
    # tower[r][c]：流经该杯的总量，可以超过 1
    tower = [[0.0] * (r + 1) for r in range(query_row + 2)]
    tower[0][0] = poured
    for r in range(query_row + 1):
        for c in range(r + 1):
            over = (tower[r][c] - 1) / 2
            if over > 0:
                tower[r+1][c] += over
                tower[r+1][c+1] += over
    return min(1.0, tower[query_row][query_glass])
```

**复杂度。** 时间 `O(R^2)`，空间 `O(R^2)`。

**易错点。**
- 把每杯限制到 1 再往下传：溢出量丢了，要保留总流量，返回时才 `min`。
- 溢出量不除以 2：左右两杯各拿一整份，`(4, 2, 1)` 得 `1.0`，应为 `0.5`。
- 只开 `query_row + 1` 行：最后一行溢出写入 `tower[r+1]` 时越界。

**追问。**
- 空间能压到 `O(R)` 吗？：能，只保留当前行滚动到下一行。

**同模式。** LC 118 杨辉三角、LC 120 三角形最小路径和、LC 688 骑士在棋盘上的概率、LC 837 新 21 点
