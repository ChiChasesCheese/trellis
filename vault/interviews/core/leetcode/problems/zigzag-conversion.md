---
slug: zigzag-conversion
---
## Q
**LC 6 Z 字形变换**｜Medium

将一个给定字符串 `s` 根据给定的行数 `numRows`，以从上往下、从左到右进行 Z 字形排列，之后从左往右逐行读取，产生新的字符串。例如 `s = "PAYPALISHIRING"`、`numRows = 3` 时排列为 `P A H N / A P L S I I G / Y I R`（第 1 行 `P`、`A`、`H`、`N`，第 2 行 `A`、`P`、`L`、`S`、`I`、`I`、`G`，第 3 行 `Y`、`I`、`R`），逐行读取为 `"PAHNAPLSIIGYIR"`。实现 `convert(s, numRows)`。`1 <= s.length <= 1000`，`s` 由英文字母（小写和大写）、`','` 和 `'.'` 组成，`1 <= numRows <= 1000`。例：`s = "PAYPALISHIRING", numRows = 4` → `"PINALSIGYAHRPI"`；`s = "A", numRows = 1` → `"A"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 模拟（simulation）：用行号的往返移动代替构造二维矩阵。

**一句话。** 按顺序把每个字符放到当前行，行号先从 `0` 加到 `numRows - 1`、再减回 `0`，来回往返；最后把各行拼起来。

**识别。** 「Z 字形排列后按行读取」只关心每个字符落在哪一行，不需要真的画出列；行号的变化规律就是往返。`n <= 1000`，任何线性方法都够。

**推导。** 直接构造二维矩阵要处理斜线部分的列号，空间 `O(n * numRows)` 且容易错。只要知道每个字符属于哪一行：下标 `i` 的字符行号随 `i` 从 `0` 一路加一到 `numRows - 1`，再一路减一回到 `0`，周而复始。用一个方向变量 `step`，碰到顶行或底行翻转，边走边把字符追加到对应行的列表里。

```python
def convert(s: str, num_rows: int) -> str:
    if num_rows == 1 or num_rows >= len(s):    # 单行或行数不少于字符数：原样输出（也避免 num_rows = 1 时方向无法翻转）
        return s
    rows: list[list[str]] = [[] for _ in range(num_rows)]
    row, step = 0, 1                           # 当前行，行号移动方向
    for ch in s:
        rows[row].append(ch)
        if row == 0:                           # 到顶：向下
            step = 1
        elif row == num_rows - 1:              # 到底：向上
            step = -1
        row += step
    return "".join("".join(r) for r in rows)
```

运行：`("PAYPALISHIRING", 3)` → `"PAHNAPLSIIGYIR"`，`("PAYPALISHIRING", 4)` → `"PINALSIGYAHRPI"`，`("A", 1)` → `"A"`，`("AB", 1)` → `"AB"`，`("ABC", 2)` → `"ACB"`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 不开各行缓冲，直接按周期算下标：周期 `cycle = 2 * numRows - 2`；第 `r` 行的字符下标是 `r + k * cycle`，非首尾行在每个周期里还多一个斜线上的字符 `(k + 1) * cycle - r`：

```python
def convert_math(s: str, num_rows: int) -> str:
    if num_rows == 1:
        return s
    cycle = 2 * num_rows - 2
    out: list[str] = []
    for r in range(num_rows):
        for i in range(r, len(s), cycle):
            out.append(s[i])
            j = i + cycle - 2 * r              # 同一周期里该行的斜线字符
            if 0 < r < num_rows - 1 and j < len(s):
                out.append(s[j])
    return "".join(out)
```

**易错点。**
- `num_rows == 1` 时顶行就是底行：`row == 0` 先让 `step = 1`，下一步 `row = 1` 就越界了，抛 `IndexError`，所以必须单独返回。
- 周期公式版本里斜线字符只属于中间行：首尾行也追加 `s[j]` 会让输出变长，`("PAYPALISHIRING", 3)` 会得到重复字符、长度超过 `14`。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 498 对角线遍历、LC 68 文本左右对齐。
