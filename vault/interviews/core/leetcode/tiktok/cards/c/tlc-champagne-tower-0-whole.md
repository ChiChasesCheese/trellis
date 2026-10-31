---
id: tlc-champagne-tower-0-whole
node: c.champagne-tower
type: qa
---
## Q
**LC 799 香槟塔**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2022-03-28（国内 CodeTop）

玻璃杯摆成金字塔：第 1 层 1 个杯子，第 2 层 2 个，依此类推到第 100 层，每个杯子容量为 1 杯。从顶层第一个杯子开始倾倒香槟，杯子满了以后溢出的部分立刻等量流向左下和右下两个杯子；最底层溢出的流到地上。现在倒入 `poured` 杯香槟，返回第 `query_row` 行第 `query_glass` 个杯子（都从 0 开始）里香槟占杯子容积的比例。`0 <= poured <= 10^9`，`0 <= query_glass <= query_row < 100`。例：`poured = 1, query_row = 1, query_glass = 1` → `0.0`；`poured = 2` 同位置 → `0.5`；`poured = 100000009, query_row = 33, query_glass = 17` → `1.0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 一整座塔倒下去：逐行模拟「流经量」，每个杯子把超过 1 的部分平分给下一行的左右两杯，答案取 `min(1, 流经量)`。

**识别。** 「从一点出发，逐层按比例传递」：状态是 `tower[行][列]`，转移只依赖上一行，天然的二维 DP（逐行推进的模拟）。不要一杯一杯地倒，`poured` 到 `10^9`。

**推导。** 暴力：每次倒一杯并传播，`O(poured · 行数)`，`10^9` 次不可行。洞察：流动是线性的，倒 `poured` 杯等价于在顶层放入 `poured` 的流量，一次性逐行向下推。`tower[r][c]` 记录流经该杯的总量（可以大于 1），溢出量是 `(tower[r][c] - 1) / 2`，加到 `tower[r + 1][c]` 和 `tower[r + 1][c + 1]`。

```python
def champagne_tower(poured: int, query_row: int, query_glass: int) -> float:
    # tower[r][c]：流经第 r 行第 c 杯的总量，可以超过 1（超出的部分会溢出）
    tower = [[0.0] * (r + 1) for r in range(query_row + 2)]   # 多开一行承接最后一行的溢出
    tower[0][0] = float(poured)
    for r in range(query_row + 1):
        for c in range(r + 1):
            overflow = (tower[r][c] - 1) / 2     # 超出 1 的部分平分给下一行的左右两杯
            if overflow > 0:
                tower[r + 1][c] += overflow
                tower[r + 1][c + 1] += overflow
    return min(1.0, tower[query_row][query_glass])    # 杯子装不下的部分已经溢出了
```

运行：`(1, 1, 1)` → `0.0`，`(2, 1, 1)` → `0.5`，`(100000009, 33, 17)` → `1.0`；`(4, 2, 0)` → `0.25`，`(4, 2, 1)` → `0.5`，`(0, 0, 0)` → `0.0`。

**复杂度。** 时间 `O(R²)`（`R = query_row`，最多约 5000 个杯子），空间 `O(R²)`。

**拓展优化。**
- 空间可以压到 `O(R)`：见 Python 工具箱「DP 降维」。
- 若某一行所有杯子的流经量都不超过 1，下面的行必然全是 0，可以提前结束。
- 需要精确值（不用浮点）：把 `tower` 换成 `fractions.Fraction`，分母都是 2 的幂，结果精确。

**易错点。**
- 把 `tower` 中的值限制到 1 再向下传：溢出量就丢了，必须保留超过 1 的总流量，返回时才 `min(1, ·)`。
- 溢出量写成 `tower[r][c] - 1` 而不除以 2：同一份溢出会被左右两杯各取一整份。`(4, 2, 1)` 应为 `0.5`，错误写法会得到 `1.0`。
- 只开 `query_row + 1` 行：最后一行的溢出写入 `tower[r + 1]` 时下标越界。

**追问。**
- 杯子容量不同或每层杯数不同：把容量换成 `cap[r][c]`，其余不变。
- 要求打印整座塔每个杯子的状态：同一张表，每格取 `min(1, tower[r][c])`。

**同模式。** LC 118 杨辉三角、LC 120 三角形最小路径和、LC 62 不同路径、LC 688 骑士在棋盘上的概率、LC 837 新 21 点。
