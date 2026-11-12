---
slug: zigzag-conversion
---
## Q
**LC 6 Z 字形变换**｜Medium

把字符串 `s` 按 `numRows` 行做 Z 字形排列（从上往下、再斜向上），然后逐行从左到右读出。例：`("PAYPALISHIRING", 3)` → `"PAHNAPLSIIGYIR"`。

## A
**一句话。** 按顺序把每个字符放到当前行，行号先加到底再减回顶，来回往返，最后把各行拼起来。

```python
def convert(s, num_rows):
    if num_rows == 1 or num_rows >= len(s):
        return s    # 单行时方向无法翻转
    rows = [[] for _ in range(num_rows)]
    row, step = 0, 1
    for ch in s:
        rows[row].append(ch)
        if row == 0:                # 到顶：向下
            step = 1
        elif row == num_rows - 1:   # 到底：向上
            step = -1
        row += step
    return "".join("".join(r) for r in rows)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- `num_rows == 1` 不单独返回：顶行就是底行，`row` 下一步变 `1` 越界抛 `IndexError`。
- 先 `row += step` 再判断顶底：到顶、到底时多走一步，行号越界。

**追问。**
- 不用模拟，直接算下标？：周期 `2 * (numRows - 1)`，首尾行每周期取一个，中间行取两个（竖线和斜线）。

**同模式。** LC 54 螺旋矩阵、LC 59 螺旋矩阵 II、LC 498 对角线遍历、LC 68 文本左右对齐
