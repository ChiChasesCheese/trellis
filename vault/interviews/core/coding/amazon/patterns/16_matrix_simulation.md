# 16 · 矩阵与模拟题：下标、边界与原地（Matrix & simulation）

矩阵和模拟题不需要新算法，考的是下标、边界和原地修改的细心程度：螺旋遍历、旋转图像、数独校验、置零、井字棋、文本排版。写之前先决定遍历方式（方向数组加转向，或四条收缩的边界），再列出边界用例（单行、单列、非方阵、空）。需要原地修改时，注意先读后写的顺序，以及把额外状态编码进已有数据的做法。每题都应该有一个用另一种方法实现的对照解来对拍。

> 本讲覆盖：LC 54 Spiral Matrix · 48 Rotate Image · 36 Valid Sudoku · 73 Set Matrix Zeroes · 348 Design Tic-Tac-Toe · 68 Text Justification（Hard）
> 前置：第 06 讲的网格与方向数组 `DIRS`、第 01 讲的计数 / `set`。本讲不需要新的算法，需要的是**细心、不变量和对「先读后写」顺序的敏感**。
> 读完你应该能：(1) 用「方向数组 + 转向」或「四条收缩的边界」两种方式遍历螺旋；(2) 用「转置 + 翻转」组合出所有旋转 / 翻转，并给出 `(i, j) → (j, n−1−i)` 的下标公式；(3) 说出「把额外状态编码进已有数据」（73 的首行首列做标记）为什么能省空间、为什么顺序不能错；(4) 把「要输出的排版」拆成「先决定每行放哪些词」和「再决定空格怎么分」两步（68）；(5) 为每道题写出**非方阵 / 单行 / 单列 / 空**这些边界测试。
> 这类题不会被问"有没有更快的算法"，而是看你**写得对不对、改得稳不稳、测试想得周不周**。每题的暴力对照解都用**另一种方法**实现，这是测试的价值所在。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

- **LC 54 螺旋遍历**：最笨的做法是维护一张同样大小的 `visited` 矩阵，朝一个方向一直走，撞墙或碰到已访问的格子就右转。它是对的，但多用 O(R·C) 空间，并且「撞墙」的判断散落在好几处。
- **LC 48 旋转图像**：新建一个同样大小的矩阵，`new[j][n-1-i] = old[i][j]`。对，但题目要求**原地**（in place），额外空间必须 O(1)。
- **LC 73 把含 0 的行列清零**：看到 0 就立刻把它所在的行和列清零——**错**：你刚写进去的 0 会被后面的扫描当成"原本就有的 0"，继续扩散，最后整张表都是 0。
- **LC 348 井字棋**：每落一子就扫描整行、整列、两条对角线判断胜负，O(n) 每步，并且要存整个棋盘 O(n²)。

### 1.2 慢在哪里 / 错在哪里

三种问题：(1) **额外内存**（`visited`、新矩阵）；(2) **读写互相干扰**（原地修改时，改过的值被当成原始值再次读到）；(3) **重复扫描**（每一步都从头判断）。

> 因果链：矩阵题的难点不在算法而在**状态管理**。→ 解法的统一思路是：用**下标公式**代替额外的数据结构（旋转、方块编号）；用**不变量**代替散落的判断（四条边界一直满足 `top ≤ bottom`、`left ≤ right`）；把必须保存的额外信息**编码到已有的数据里**（首行首列当标记）；用**计数器**代替整张表（井字棋每行每列一个整数）。

### 1.3 矩阵与模拟题的工具箱（从零讲）

- **表示**：`matrix[r][c]`，`rows = len(matrix)`，`cols = len(matrix[0])`。先问空矩阵（`[]` 和 `[[]]` 是两种不同的空）。最常见的低级 bug 是行列写反。
- **用 `[[0] * c] * r` 创建矩阵是错的**：`*` 复制的是**同一个行列表的引用**，修改一行等于修改所有行。要用 `[[0] * c for _ in range(r)]`。
- **方向数组**：`DIRS = ((0,1), (1,0), (0,-1), (-1,0))`（右、下、左、上，恰好是顺时针顺序）。"右转"就是 `d = (d + 1) % 4`。
- **常用下标公式**（背下来）：
  - 展平：`idx = r * cols + c`，还原：`r, c = divmod(idx, cols)`。
  - 主对角线：`r == c`；副对角线：`r + c == n − 1`；同一条 "\" 线上 `r − c` 相同，同一条 "/" 线上 `r + c` 相同。
  - 数独的 3×3 宫编号：`(r // 3) * 3 + c // 3`。
  - 顺时针旋转 90°：`(i, j) → (j, n − 1 − i)`。
- **旋转 / 翻转 = 组合**：顺时针 90° = **转置**（沿主对角线交换）+ **每行左右翻转**；逆时针 90° = 每行翻转 + 转置（或转置 + 上下翻转）；180° = 上下翻转 + 左右翻转。记住这个组合，就不用背四种旋转的公式。
- **原地编码**：当需要保存的额外信息很小（一位、一个状态），可以借用数据里**已知不会冲突**的位置（73 的首行首列），或者给每个格子多编码几位（Game of Life LC 289：用 2 位同时存"旧状态"和"新状态"）。铁律：**标记必须在被覆盖之前被消费**。
- **「决定」与「格式化」分开**（68）：先用贪心决定每行放哪些词，再单独处理空格分配。不要在一个循环里同时做两件事。
- **测试矩阵题的固定清单**：`1×1`、`1×N`、`N×1`、非方阵、空矩阵、奇数 / 偶数边长、全相同值、边界上的特殊值，以及"暴力对拍"（用**另一种方式**实现的对照解）和**性质测试**（旋转 4 次回到原样）。

## 2. 模板与逐行讲解

```python
# Template M1: the direction vector + "turn right when blocked" walk (the visited-matrix way to spiral)
DIRS4 = ((0, 1), (1, 0), (0, -1), (-1, 0))        # right, down, left, up: clockwise order

def spiral_cells(rows, cols):
    seen = [[False] * cols for _ in range(rows)]  # NOT [[False] * cols] * rows: that aliases one row
    r = c = d = 0
    for _ in range(rows * cols):
        yield r, c
        seen[r][c] = True
        nr, nc = r + DIRS4[d][0], c + DIRS4[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols) or seen[nr][nc]:
            d = (d + 1) % 4                       # blocked: turn right
            nr, nc = r + DIRS4[d][0], c + DIRS4[d][1]
        r, c = nr, nc


# Template M2: indexing helpers -- rotation as a formula, rotation as "transpose + reverse", flatten / unflatten, sudoku box
def rotate_cw_new(m):                             # allocating version: the clean reference
    return [list(row) for row in zip(*m[::-1])]

def rotated_position(i, j, n):                    # where cell (i, j) of an n x n matrix lands after a clockwise quarter turn
    return j, n - 1 - i

def box_id(r, c):
    return r // 3 * 3 + c // 3

m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
cells = list(spiral_cells(3, 4))
assert [m[r][c] for r, c in cells] == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert sorted(cells) == [(r, c) for r in range(3) for c in range(4)]     # every cell exactly once
assert list(spiral_cells(1, 1)) == [(0, 0)] and list(spiral_cells(1, 3)) == [(0, 0), (0, 1), (0, 2)]
assert list(spiral_cells(3, 1)) == [(0, 0), (1, 0), (2, 0)]

sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
turned = rotate_cw_new(sq)
assert turned == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
assert all(turned[rotated_position(i, j, 3)[0]][rotated_position(i, j, 3)[1]] == sq[i][j] for i in range(3) for j in range(3))
assert rotate_cw_new(rotate_cw_new(rotate_cw_new(rotate_cw_new(sq)))) == sq    # 4 turns = identity (a property test)
assert all(divmod(r * 5 + c, 5) == (r, c) for r in range(4) for c in range(5))
assert sorted({box_id(r, c) for r in range(9) for c in range(9)}) == list(range(9)) and box_id(4, 7) == 5
```

逐行讲解：

1. `DIRS4` 的顺序是**顺时针**，所以"右转"是 `(d + 1) % 4`；如果顺序写成上下左右，转向就要查表。
2. `seen = [[False] * cols for _ in range(rows)]`：每一行是独立的新列表（别名陷阱见 1.3）。
3. `if not (in bounds) or seen[nr][nc]`：两个"被挡住"的情形合在一处：撞墙、碰到走过的格子。这就是 M1 与 4.1 的边界版相比的优点（判断集中）和缺点（多 O(R·C) 空间）。
4. `for _ in range(rows * cols)`：总共输出 R·C 个格子，**用计数而不是"是否还有未访问的格子"来终止**，避免死循环。
5. `rotate_cw_new`：`m[::-1]` 把行倒过来，`zip(*...)` 把列变成行——合起来就是顺时针旋转；它分配了新矩阵，所以只作为对照解和下标公式的验证。
6. `rotated_position`：原来在第 `i` 行第 `j` 列的格子，旋转后到第 `j` 行第 `n−1−i` 列。断言逐格验证。
7. 性质测试：连续旋转四次必须回到原样——不依赖任何对照解就能抓到一大类 bug。

## 3. 完整手算（Worked trace）

下面是真实运行结果：先把 3×4 的矩阵用「四条边界」方式走一遍螺旋（第二圈会触发两个保护条件），再把 3×3 旋转拆成转置 + 翻转。

```python
def spiral_trace(matrix):
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out, ring = [], 0
    while top <= bottom and left <= right:
        ring += 1
        print(f"ring {ring}: top={top} bottom={bottom} left={left} right={right}")
        row = [matrix[top][c] for c in range(left, right + 1)]
        out += row
        print(f"   right along row {top}: {row}")
        top += 1
        col = [matrix[r][right] for r in range(top, bottom + 1)]
        out += col
        print(f"   down column {right}: {col}")
        right -= 1
        if top <= bottom:
            row = [matrix[bottom][c] for c in range(right, left - 1, -1)]
            out += row
            print(f"   left along row {bottom}: {row}")
            bottom -= 1
        else:
            print("   guard top <= bottom failed: no bottom row to walk back")
        if left <= right:
            col = [matrix[r][left] for r in range(bottom, top - 1, -1)]
            out += col
            print(f"   up column {left}: {col}")
            left += 1
        else:
            print("   guard left <= right failed: no left column to walk back")
    return out

m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
assert spiral_trace(m) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
print()

def show(label, m):
    print(f"{label:<22}" + " | ".join(" ".join(f"{x:2}" for x in row) for row in m))

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
show("start", m)
for i in range(3):
    for j in range(i + 1, 3):
        m[i][j], m[j][i] = m[j][i], m[i][j]
show("after transpose", m)
for row in m:
    row.reverse()
show("after reversing rows", m)
assert m == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
print("cell (0,1)=2 moved to (1,2): formula (i, j) -> (j, n-1-i) gives", (1, 3 - 1 - 0))
```

```text
ring 1: top=0 bottom=2 left=0 right=3
   right along row 0: [1, 2, 3, 4]
   down column 3: [8, 12]
   left along row 2: [11, 10, 9]
   up column 0: [5]
ring 2: top=1 bottom=1 left=1 right=2
   right along row 1: [6, 7]
   down column 2: []
   guard top <= bottom failed: no bottom row to walk back
   up column 1: []

start                  1  2  3 |  4  5  6 |  7  8  9
after transpose        1  4  7 |  2  5  8 |  3  6  9
after reversing rows   7  4  1 |  8  5  2 |  9  6  3
cell (0,1)=2 moved to (1,2): formula (i, j) -> (j, n-1-i) gives (1, 2)
```

怎么读：

- **第一圈**走完四条边；第二圈只剩一行（`top = bottom = 1`）：往右走 `[6, 7]` 之后 `top` 变成 2、超过了 `bottom`，此时如果不加 `if top <= bottom` 就会把第 1 行再往左走一遍，输出 `7, 6`——重复。
- 同样，`left <= right` 的保护防止"只剩一列"时往上走重复。**两个 `if` 不是可有可无的，它们是单行 / 单列边界的全部内容。**
- **旋转**：转置之后第一行是原来的第一列 `1 4 7`；再把每一行翻转得到 `7 4 1`，正好是顺时针 90° 的结果。最后一行验证公式：原来 `(0, 1)` 处的 `2` 现在在 `(1, 2)`，与 `(i, j) → (j, n−1−i)` 一致。

## 4. 题目

### 4.1 LC 54 · Spiral Matrix（Medium）

```python
# solutions/54_spiral_matrix.py
def spiral_order(matrix):
    if not matrix or not matrix[0]:
        return []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):               # -> along the top row
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):               # v down the right column
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                              # a single remaining row must not be walked back
            for c in range(right, left - 1, -1):       # <- along the bottom row
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                              # a single remaining column must not be walked back
            for r in range(bottom, top - 1, -1):       # ^ up the left column
                out.append(matrix[r][left])
            left += 1
    return out
```

- **一句话洞见**：四条边界 `top / bottom / left / right` 一圈一圈向内收缩；每走完一条边就收缩对应的边界；走"回头"的两条边之前必须先检查边界没有交叉。
- **复杂度**：时间 O(R·C)，除了输出列表以外空间 O(1)（对比 M1 的 O(R·C) `seen`）。
- 变体：LC 59 Spiral Matrix II（按螺旋顺序**填**数）用同一个循环，把 `out.append(...)` 换成赋值；逆时针只需调换顺序。

**资深追问**

- **规模 ×1000**：矩阵太大不能整个物化 → 写成**生成器**（`yield`），按需产出；也可以直接用下标公式算出"第 k 个元素在哪"，随机访问 O(1)（先算在第几圈，再算圈内位置）。
- **流式**：按螺旋顺序产出的元素，调用方可以边消费边处理，内存 O(1)。
- **内存**：边界版 O(1)；`seen` 版 O(R·C)。
- **并发**：每一圈互相独立（圈的起点和长度由公式确定），可以并行计算每圈的输出，再按圈序拼接。
- **接口**：返回列表还是迭代器；参差（jagged）矩阵怎么办（先校验每行等长）；空矩阵 `[]` 与 `[[]]` 都返回 `[]`。
- **测试**：`1×1`、`1×N`、`N×1`、非方阵（3×4 与 4×3）、奇数 / 偶数边长；与「方向数组 + `seen`」对拍（用它作为对照解）。

### 4.2 LC 48 · Rotate Image（Medium）

```python
# solutions/48_rotate_image.py
def rotate(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):                      # transpose: swap across the main diagonal
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()                                  # mirror left <-> right


def rotate_by_cycles(matrix):                          # the "four cells at a time" version interviewers sometimes ask for
    n = len(matrix)
    for i in range(n // 2):
        for j in range(i, n - 1 - i):
            tmp = matrix[i][j]
            matrix[i][j] = matrix[n - 1 - j][i]                   # left   -> top
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]   # bottom -> left
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]   # right  -> bottom
            matrix[j][n - 1 - i] = tmp                            # top    -> right
```

- **一句话洞见**：顺时针旋转 90° = **先转置，再把每一行左右翻转**。两步都是原地的，总共 O(n²) 时间、O(1) 空间。转置时 `j` 从 `i + 1` 开始：只交换上三角和下三角各一次，若遍历整个矩阵会交换两次、等于什么都没做。
- **四元环版本**（`rotate_by_cycles`）：旋转把格子分成 4 个一组的环（上→右→下→左→上），一次处理四个格子，只需一个临时变量。面试官有时会要求"不要借助转置"，这是备选。
- **复杂度**：时间 O(n²)，空间 O(1)。

**资深追问**

- **规模 ×1000**：图像大到放不下内存（磁盘上的 100 000 × 100 000 图片）：按**块**读入（tiling），每个 `B × B` 的块在内存里旋转后写到目标位置；对 IO 顺序要小心，因为列方向访问行主序存储的数组缓存很差。
- **流式**：不要真的旋转——保存一个"变换标志"（0/90/180/270 度），读取时用下标公式映射 `(i, j) → …`；多次旋转只是标志相加 mod 4。这是图像库（视图 view / stride）的常见做法。
- **内存**：原地 O(1)；对非方阵（`R × C`）**无法**原地（形状会变），必须新分配。
- **并发**：四元环互相独立，可以按环分块并行；转置 + 翻转版本可以按行块并行（转置时每对 `(i, j)` 只被一个线程处理）。
- **接口**：原地修改并返回 `None`（LeetCode 约定）；元素是像素结构体（RGB）时交换的是整个结构体，不是单个通道；顺时针还是逆时针要问清楚。
- **测试**：`1×1`、`2×2`、奇数边长（中心格子不动）；旋转 4 次回到原样（性质测试）；与 `zip(*m[::-1])` 对拍（同时验证两种原地实现）。

### 4.3 LC 36 · Valid Sudoku（Medium）

```python
# solutions/36_valid_sudoku.py
def is_valid_sudoku(board):
    rows, cols, boxes = [0] * 9, [0] * 9, [0] * 9
    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == ".":
                continue
            bit = 1 << (int(ch) - 1)
            b = r // 3 * 3 + c // 3                     # box index 0..8
            if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                return False                            # digit seen before in this row, column or box
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
    return True                                         # validity only: the puzzle may still be unsolvable
```

- **一句话洞见**：一遍扫描，对每个非空格子，用位掩码检查它的数字是否已出现在它所在的**行、列、宫**中；三个约束三个掩码数组。宫编号 `r // 3 * 3 + c // 3`。
- **注意**：它只检查**已填的数字不冲突**，不保证谜题**有解**——有解性是 LC 37（第 12 讲）的问题。
- **复杂度**：固定 81 格，O(1)（推广到 n×n 是 O(n²)）。

**资深追问**

- **规模 ×1000**：×1000 个棋盘 → 彼此独立，天然并行；推广到 n×n（n = 16, 25）只需改宫的边长（`√n`）。
- **流式**：玩家一步一步落子：不要每步重新校验整盘，只检查**被改动的那个格子**所在的行 / 列 / 宫是否冲突（O(1)），并增量维护掩码；撤销一步就清除对应的位。
- **内存**：27 个整数，O(1)。
- **并发**：行、列、宫三类校验互相独立，可以三个任务并行；但这里规模太小，并行没有意义——要敢说"不值得"。
- **接口**：数字是字符还是整数；`.` 还是 `0` 表示空；返回布尔值，还是**返回冲突的位置**（用户体验更好、调试也更容易）；输入尺寸或字符非法时抛异常还是返回 `False`。
- **测试**：宫内冲突但行列不冲突（专门测一个）、整行冲突、整列冲突、全空棋盘、合法的完整解；与「分别检查行 / 列 / 宫」的暴力版对拍。

### 4.4 LC 73 · Set Matrix Zeroes（Medium）

```python
# solutions/73_set_matrix_zeroes.py
def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))      # these two flags remember the markers' own state
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0                       # mark row r and column c
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:                                                # LAST: the markers were still needed above
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
```

- **先说 O(R + C) 的解法**：第一遍扫描把含 0 的行号、列号记入两个集合；第二遍清零。这个解简单、不容易错，面试里先讲它，然后再说"如果要求 O(1) 额外空间"。
- **O(1) 空间的一句话洞见**：用**第一行和第一列**当作标记数组（`matrix[r][0] = 0` 表示第 `r` 行要清零，`matrix[0][c] = 0` 表示第 `c` 列要清零）；但首行首列本身是否原本含 0，需要先用两个布尔变量记下来。**顺序**：(1) 记下首行首列是否有 0；(2) 用内部格子的 0 在首行首列打标记；(3) 根据标记清零内部格子；(4) **最后**才根据 (1) 的两个布尔值清零首行首列——如果提前清掉，标记就丢了。
- **复杂度**：时间 O(R·C)，空间 O(1)（集合版 O(R + C)）。

**资深追问**

- **规模 ×1000**：矩阵在磁盘上：第一遍只收集含 0 的行号 / 列号（O(R + C) 位的位图），第二遍流式重写——比 O(1) 技巧更实用，因为 O(1) 技巧要随机读写。
- **流式**：数据以行流到达：对每一行判断是否含 0、同时累积"含 0 的列"位图；行内容已经输出过的无法追加清零，所以必须两遍或缓冲。
- **内存**：集合版位图 R + C 位；就地版 O(1)。
- **并发**：第一遍可以按行分块并行，各自产出本块的"零行 / 零列"，再合并（求并集）；第二遍并行清零，互不冲突。
- **接口**：原地修改，返回 `None`；元素不一定是整数（`0.0`、`None`）时"零"的定义；稀疏矩阵的表示（只存非零坐标）下，这题变成集合运算。
- **测试**：首行有 0、首列有 0、两者都有、`[[0]]`、`1×N`、`N×1`、没有 0（不变）；对拍的对照解是"集合版"。**特别注意**：被标记写出的 0 不是新 0——这是顺序错误最典型的症状。

### 4.5 LC 348 · Design Tic-Tac-Toe（Medium）

```python
# solutions/348_design_tic_tac_toe.py
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = 0                                   # cells with row == col
        self.anti = 0                                   # cells with row + col == n - 1

    def move(self, row, col, player):
        """Returns the winning player (1 or 2) if this move completes a line, else 0. Assumes a legal move."""
        delta = 1 if player == 1 else -1                # a full line of one player has |count| == n
        n = self.n
        self.rows[row] += delta
        self.cols[col] += delta
        won = abs(self.rows[row]) == n or abs(self.cols[col]) == n
        if row == col:
            self.diag += delta
            won = won or abs(self.diag) == n            # look at a diagonal only if THIS move is on it
        if row + col == n - 1:
            self.anti += delta
            won = won or abs(self.anti) == n
        return player if won else 0
```

- **一句话洞见**：不存棋盘。每行、每列、两条对角线各一个计数器：玩家 1 落子 `+1`，玩家 2 落子 `−1`。一条线上的计数绝对值等于 `n`，说明这条线全是同一个玩家的棋子。每次落子 O(1)，内存 O(n)。
- **一个微妙之处**：只检查**这次落子所在**的行、列、以及（如果在对角线上）对角线。如果每次都检查两条对角线的计数，在对角线已经被某位玩家占满之后，其他位置的后续落子会被误判为获胜——随机对拍（整盘落满而不在获胜时停止）就是用来抓这个 bug 的。
- **复杂度**：`move` O(1)，空间 O(n)。

**资深追问**

- **规模 ×1000**：棋盘变成 10⁹ × 10⁹ 的"五子棋"（连成 K 个才赢，不是整行）→ 整行计数不再够用；改用稀疏 `dict` 存落子，每次落子沿 4 个方向统计连续同色的数量（需要往两侧延伸，O(K)）。
- **流式**：这类问题本身就是在线的：每个 `move` 立即返回结果。
- **内存**：O(n) 对 O(n²)；稀疏棋盘 O(落子数)。
- **并发**：同一局内的落子必须串行（轮流）；多局之间互相独立，按局 ID 分片，每局一把锁（或每局一个 actor）。
- **接口**：**非法落子**（格子已占用、不是该玩家的回合、游戏已结束）要怎么处理——题目假设落子合法，真实系统要校验并拒绝（需要保存棋盘或占用位图）；是否支持悔棋（`undo`：反向计数，需要保存历史）；返回胜者还是状态枚举（进行中 / 平局 / 胜者）。
- **测试**：整行、整列、主对角线、副对角线各一个；`n = 1`（第一步就赢）；落子顺序随机的整盘对拍（用完整棋盘扫描作对照解）。

### 4.6 LC 68 · Text Justification（Hard）

```python
# solutions/68_text_justification.py
def full_justify(words, max_width):
    lines, i, n = [], 0, len(words)
    while i < n:
        j, used = i, len(words[i])                     # words[i..j] fit; `used` counts letters plus single spaces
        while j + 1 < n and used + 1 + len(words[j + 1]) <= max_width:
            j += 1
            used += 1 + len(words[j])
        group = words[i:j + 1]
        if j == n - 1 or len(group) == 1:              # last line, or a line that has no gap to stretch
            line = " ".join(group)
            line += " " * (max_width - len(line))
        else:
            slack = max_width - sum(len(w) for w in group)
            gaps = len(group) - 1
            each, extra = divmod(slack, gaps)          # the LEFTMOST `extra` gaps get one more space
            line = "".join(w + " " * (each + (1 if k < extra else 0)) for k, w in enumerate(group[:-1])) + group[-1]
        lines.append(line)
        i = j + 1
    return lines
```

- **一句话洞见**：两步。(1) **贪心装行**：尽量往一行里放词，每个词之间至少一个空格，放不下就换行；(2) **分配空格**：用 `divmod(多余空格, 空隙数)` 得到每个空隙的基础空格数和需要多一个空格的空隙数，**多出来的空格给最左边的空隙**。两个特例：最后一行和只有一个单词的行都是**左对齐**（右侧补空格）。
- **为什么算 Hard**：算法一点都不难，难的是规则很多、很容易漏一条——单词行除零（`gaps = 0`）、最后一行不拉伸、宽度判断里别忘了单词之间的那个空格（`+ 1`）。
- **复杂度**：时间 O(总字符数)，空间 O(输出)。注意用 `"".join(...)` 而不是反复 `+=` 拼接（字符串不可变，每次拼接都是新分配，会退化成 O(n²)）。

**资深追问**

- **规模 ×1000**：整本书的排版 → 写成**生成器**逐行产出，内存 O(最大行宽)；段落之间互相独立，可以并行。
- **流式**：词流式到达：维护当前行的词缓冲，放不下就输出当前行，天然流式；只有"最后一行"需要流结束的信号。
- **内存**：生成器版 O(行宽)。
- **并发**：同一段落内行与行是顺序依赖的（贪心），不可并行；跨段落可以。
- **接口**：单词比行宽还长怎么办（拒绝 / 断词 / 允许溢出）；单词中含空格、制表符；**宽度不等于字符数**（CJK 全角字符占两格、组合字符占零格 → 用 `wcwidth` 类的库）；是否需要连字符断词；末尾空格要不要保留。
- **测试**：不要只测几个例子，写一个**性质检查器**：单词顺序不变、每行恰好 `width` 个字符、每一行都是**贪心最大**（下一个词确实放不下）、非末尾多词行的空隙差不超过 1 且左大右小、最后一行 / 单词行是左对齐。随机输入下这些性质同时成立，比对比固定样例强得多。

## 5. 常见 bug

1. **行列写反**：`len(matrix)` 是行数，`len(matrix[0])` 才是列数；非方阵一测就暴露。
2. **`[[0] * c] * r` 别名**：所有行是同一个列表。用推导式。
3. **空矩阵**：`matrix[0]` 在 `[]` 上越界；`[[]]` 的列数是 0。先判断。
4. **螺旋遍历漏掉保护条件**：只剩一行 / 一列时重复输出（3 节的第二圈）。
5. **转置遍历了整个矩阵**：每对 `(i, j)` 被交换两次，等于没转；`j` 从 `i + 1` 开始。
6. **顺时针和逆时针搞反**：转置 + **翻转每一行** = 顺时针；翻转行的顺序（上下翻）+ 转置 = 逆时针。
7. **73 过早清零首行 / 首列**：它们是标记数组，必须最后处理；用标记写出的 0 当成原始的 0 会让整张表被清零。
8. **数独宫编号公式**：`r // 3 * 3 + c // 3`；写成 `r // 3 + c // 3` 会让不同的宫共用编号。
9. **348 检查所有计数器而不只检查被影响的**：对角线占满之后，后续落子被误判获胜。副对角线条件是 `row + col == n − 1`。
10. **68 的宽度判断少算一个空格**：`used + 1 + len(word) <= width`；单词行 `gaps = 0` 时除零；最后一行被拉伸。
11. **用 `+=` 反复拼接大字符串**：O(n²)；收集到列表再 `join`。

## 6. 自测题

1. 为什么顺时针旋转 90° 等于「转置 + 每行翻转」？用 `(i, j)` 的下标证明。
   <details><summary>答案</summary>转置把 `(i, j)` 移到 `(j, i)`；翻转每一行把列下标 `j'` 变成 `n − 1 − j'`，所以 `(j, i)` 移到 `(j, n − 1 − i)`。这正是顺时针旋转的公式 `(i, j) → (j, n − 1 − i)`。</details>
2. 为什么 `[[0] * 3] * 3` 不能用来创建 3×3 矩阵？写出正确写法。
   <details><summary>答案</summary>`*` 复制的是内层列表的引用，三行是同一个对象，改一格等于改三行。正确：`[[0] * 3 for _ in range(3)]`。</details>
3. 73 题里，为什么要最后才清零首行和首列？
   <details><summary>答案</summary>首行首列同时承担"标记数组"的角色：内部格子是否要清零要读它们。如果先清零，标记丢失，内部格子就无法正确判断；所以先记下首行首列原本是否有 0（两个布尔值），用标记清完内部格子之后，最后再根据那两个布尔值处理首行首列。</details>
4. 小编程：写出逆时针旋转 90° 的原地版本。
   <details><summary>答案</summary>先转置（`j` 从 `i + 1` 开始交换），再把**行的顺序**上下翻转（`matrix.reverse()`），或者先每行翻转再转置也可以。验证：`[[1,2],[3,4]]` → 转置 `[[1,3],[2,4]]` → 上下翻转 `[[2,4],[1,3]]`，等于逆时针旋转。</details>
5. 348 的计数器方案为什么只需要检查"被这次落子影响的"那几条线？
   <details><summary>答案</summary>一次落子只改变它所在的行、列和（若在对角线上）对角线的计数；其他线的计数没变，上一步没赢就不会因为这一步而赢。检查无关线路不仅多余，还会在某条线早就被占满后产生误判。</details>
6. 68 题怎样证明你的实现"正确"？你会写哪些性质测试？
   <details><summary>答案</summary>词序不变；每行长度恰为 `width`；贪心最大性（下一个词放不进去）；非末行多词行的空隙差 ≤ 1 且多的空格在左；末行与单词行左对齐且右补空格；再加手写的样例和随机输入。性质测试比固定样例能覆盖更多边界。</details>
7. 资深追问：一个图像服务每秒要旋转几千张大图，你怎么设计？
   <details><summary>答案</summary>优先**不旋转**：保存方向元数据（EXIF 式），渲染 / 读取时做下标映射；确实要物化时按块（tiling）旋转，使读写都尽量顺序，利用 SIMD / GPU；并行单位是块；按图片分片到 worker；非方阵需要分配新缓冲区；监控内存峰值与尾延迟，对超大图限流。</details>
