---
id: tlc-n-queens-2-code
node: a.n-queens
type: qa
step: 2
---
## Q
**LC 51 N 皇后**｜写出 Python 实现

整数 `n`（`1 <= n <= 9`）。返回把 `n` 个皇后放在 `n x n` 棋盘上互不攻击的所有摆法；每种摆法是由 `n` 个长度为 `n` 的字符串组成的列表，`'Q'` 表示皇后，`'.'` 表示空位。

## A
**思路。** 逐行放置。`cols[r]` 记录第 `r` 行皇后所在的列；`used_col`、`used_diag`（`r - c`）、`used_anti`（`r + c`）三个集合记录已占用的列和两个方向的斜线。每一行尝试所有列，不冲突就放下并递归下一行，返回后撤销。放满 `n` 行时按 `cols` 生成棋盘字符串。

```python
def solve_n_queens(n: int) -> list[list[str]]:
    result: list[list[str]] = []
    cols: list[int] = []                           # cols[r] = 第 r 行皇后所在的列
    used_col: set[int] = set()
    used_diag: set[int] = set()                    # 主对角线（左上-右下）：r - c 相同
    used_anti: set[int] = set()                    # 副对角线（右上-左下）：r + c 相同

    def place(r: int) -> None:
        if r == n:
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            return
        for c in range(n):
            if c in used_col or r - c in used_diag or r + c in used_anti:
                continue
            cols.append(c)
            used_col.add(c)
            used_diag.add(r - c)
            used_anti.add(r + c)
            place(r + 1)
            used_anti.remove(r + c)
            used_diag.remove(r - c)
            used_col.remove(c)
            cols.pop()

    place(0)
    return result
```

运行：`n = 4` → `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`；`n = 1` → `[["Q"]]`；`n = 1` 到 `9` 的解数 `[1, 0, 0, 2, 10, 4, 40, 92, 352]`。

**复杂度。** 时间 `O(n!)` 上界，实际远小于；空间 `O(n)`（不含输出）。

**写法要点。** 三个 `set` 让冲突检测是 `O(1)`；`cols` 只存每行的列，生成字符串时才展开成棋盘，比维护二维数组轻；字符串用 `"." * c + "Q" + "." * (n - c - 1)` 拼成，避免逐字符修改（Python 字符串不可变）；撤销顺序与加入顺序相反，只是习惯，三个集合互不影响；`n = 2, 3` 无解时 `result` 保持为空列表。
