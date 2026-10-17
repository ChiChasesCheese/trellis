# 12 · 回溯：选择 → 递归 → 撤销（Backtracking）

> 本讲覆盖：LC 22 Generate Parentheses · 17 Letter Combinations of a Phone Number · 79 Word Search · 78 Subsets（附 90 带重复、46 全排列）· 51 N-Queens（Hard，附 52）· 37 Sudoku Solver（Hard）
> 前置：第 06 讲的 DFS / 递归调用栈；Python `list.append` / `list.pop`；知道「列表是引用」（改一处，所有拿着它的人都看到）。
> 读完你应该能：(1) 把任何「枚举所有方案 / 找一个满足约束的方案」的题画成一棵**决策树**；(2) 默写 choose → explore → un-choose 模板，并说清每个撤销为什么必须有；(3) 在「子集型 / 排列型 / 可重复组合型」三种分支规则里选对一个；(4) 说出剪枝剪掉的是什么，并回答「输出本身就是指数级，怎么办」这类资深追问。
> 这一讲和前 11 讲不同：回溯的复杂度通常是**指数级**，面试考的不是「把它变成多项式」，而是「剪枝多狠、状态维护多干净、输出规模如何处理」。

## 1. 这个模式是什么，为什么存在

### 1.1 从最笨的解法开始

LC 22：给定 `n` 对括号，列出所有合法的括号串。`n = 2` 时答案是 `(())` 和 `()()`。

最笨的做法：先把所有由 `(` 和 `)` 组成、长度 `2n` 的串都生成出来（`2^(2n)` 个），再逐个检查是否合法。`n = 2` 时是 16 个串，只有 2 个合法；`n = 10` 时是 1 048 576 个串，合法的只有 16 796 个（卡特兰数，Catalan number）。

LC 78 Subsets 的最笨做法类似：对 `n` 个元素，枚举 `0 … 2^n − 1` 的每个整数，把二进制位当作「选 / 不选」。这个做法其实**是对的**，而且很干净（后面会作为交叉验证用）；它的问题是只能做「无约束的全枚举」——一旦题目说「和必须等于 target」「不能攻击」，它就无法在中途放弃一个明显没希望的方案。

### 1.2 慢在哪里 / 错在哪里

生成再过滤把**所有**串都构造到最后一个字符才检查。可是 `)(…` 这个前缀在第一个字符就已经非法了，以它开头的 `2^(2n−1)` 个串全是白费功夫。

> 因果链：答案是**一步一步构造出来**的（每一步选一个字符 / 一个元素 / 一个格子里的数字）→ 把这个过程画成一棵树（根 = 什么都没选，每条边 = 一次选择，叶子 = 一个完整方案）→ 在每个**内部节点**就检查约束，违反就整棵子树不再展开（**剪枝，pruning**）→ 只访问合法的前缀。这就是回溯：深度优先地走这棵树，走不通就退回上一步换一个选择。

### 1.3 回溯是什么（从零讲）

- **决策树（state-space tree）**：根是空方案；第 `k` 层的节点代表「已经做完前 `k` 个决定」；叶子是完整方案。回溯 = 对这棵树做 DFS。你**不会真的把树存下来**，递归调用栈就是当前走到的那条路径。
- **三个动作**（背下来）：
  1. **choose**：把一个选择加入当前方案（`path.append(x)`，同时更新「已用集合」之类的辅助状态）。
  2. **explore**：递归去处理下一个决定（`go(...)`）。
  3. **un-choose**：把刚才加入的选择**原样撤销**（`path.pop()`，辅助状态还原），让同一层的下一个选择看到一模一样的现场。
- **为什么要撤销**：`path` 是**一个**共享的可变列表，所有递归层都在读写它。如果不撤销，兄弟分支会看到上一个分支留下的垃圾。撤销的代价 O(1)，比「每层都复制一份 `path`」便宜得多（后者每层 O(n)）。
- **为什么记录答案时要拷贝**：`out.append(path)` 存的是**同一个列表的引用**；之后 `path` 被继续修改（最后被 pop 到空），`out` 里所有元素都变成 `[]`。必须 `out.append(path[:])`（或 `list(path)`）。
- **剪枝**：在 choose 之前检查约束（`if not allowed: continue`）或在递归入口检查。剪枝点越靠前越好。
- **三种分支规则**（决定「这一层可选哪些元素」，也决定怎么避免重复）：
  - **子集 / 组合型**：顺序不重要，选了 `nums[i]` 之后下一层只能从 `i+1` 开始选（传 `start` 参数）。这样 `{1,2}` 只会以 `[1,2]` 出现，不会再出现 `[2,1]`。
  - **排列型**：顺序重要，每层都可以选任何**还没用过**的元素（`used[]` 标记，同样需要撤销）。
  - **可重复组合型**（LC 39）：同一个元素可以反复用，下一层仍从 `i` 开始（传 `i` 而不是 `i+1`）。
- **去重**：输入含重复元素（LC 90 / 47 / 40）时，先**排序**，然后在**同一层**里跳过「和前一个相同的值」（`if i > start and nums[i] == nums[i-1]: continue`）。注意是「同一层」：不同层可以选同一个值（`[2,2]` 是合法子集）。
- **复杂度怎么说**：回溯的时间 ≈ 「树里被访问的节点数 × 每个节点的工作量」。最坏是指数级；要说清「叶子数」（例如 Subsets 是 2^n，Permutations 是 n!，括号是卡特兰数 ≈ 4^n / n^1.5）以及「每个叶子复制答案的成本」（O(n)）。
- **递归深度**等于决策的步数（括号 2n，子集 n，数独 81），远小于 Python 的默认限制 1000——这是回溯和第 06 讲 DFS 的区别：深度小，宽度爆炸。

## 2. 模板与逐行讲解

```python
# Template B0 -- the skeleton (every backtracking problem is this with different `allowed` / `record` / `next`):
#
#   def go(state):
#       if is_complete(state):
#           record(copy_of(state))      # COPY: the live state keeps changing
#           return
#       for choice in candidates(state):
#           if not allowed(state, choice):
#               continue                # prune BEFORE recursing
#           apply(choice)               # choose
#           go(next_state)              # explore
#           undo(choice)                # un-choose: restore the exact previous state

# Template B1: combination sum (LC 39) -- elements may be reused, so the recursion passes `i`, not `i + 1`
def combination_sum(candidates, target):
    candidates = sorted(candidates)
    out, path = [], []

    def go(start, remain):
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                        # sorted: every later candidate is too big as well
            path.append(candidates[i])
            go(i, remain - candidates[i])    # i, not i + 1: the same element may be used again
            path.pop()

    go(0, target)
    return out


# Template B2: combinations C(n, k) (LC 77) -- prune by counting how many numbers are still available
def combinations_nk(n, k):
    out, path = [], []

    def go(start):
        if len(path) == k:
            out.append(path[:])
            return
        need = k - len(path)
        for i in range(start, n - need + 2):  # numbers i..n must still contain `need` elements
            path.append(i)
            go(i + 1)
            path.pop()

    go(1)
    return out


from itertools import combinations

assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
assert combination_sum([2], 1) == []
assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert combinations_nk(4, 2) == [list(c) for c in combinations(range(1, 5), 2)]
assert combinations_nk(5, 5) == [[1, 2, 3, 4, 5]] and combinations_nk(3, 1) == [[1], [2], [3]]
assert all(combinations_nk(n, k) == [list(c) for c in combinations(range(1, n + 1), k)]
           for n in range(1, 8) for k in range(1, n + 1))
```

逐行讲解：

1. **B0 骨架**：六行就是全部。`is_complete` 决定什么时候记录答案；`candidates` 决定这一层有哪些分支；`allowed` 是剪枝；`apply` / `undo` **必须成对**，而且 `undo` 要把状态恢复到 `apply` 之前一模一样（包括 `used[]`、`set`、计数器）。
2. **B1 的 `break` 而不是 `continue`**：`candidates` 已排序，当前这个数超过 `remain` 时后面的更大，直接 `break` 整个 for 循环——这是比「检查再 `continue`」更强的剪枝。如果没排序就只能 `continue`。
3. **B1 的 `go(i, …)`**：传 `i` 表示「下一层还可以选 `candidates[i]`」（可重复使用）；同时因为下一层只从 `i` 开始，`[3,2,2]` 不会出现（顺序固定为非降序），所以不会产生重复组合。把它改成 `i + 1` 就变成「每个数只能用一次」（LC 40，还要加去重）。
4. **B1 的 `path[:]`**：见 1.3，拷贝。
5. **B2 的 `range(start, n - need + 2)`**：已经选了 `len(path)` 个，还差 `need` 个；从 `i` 开始还剩 `n - i + 1` 个数，必须 `n - i + 1 >= need`，即 `i <= n - need + 1`，所以上界（不含）是 `n - need + 2`。这个剪枝把「注定凑不够」的分支在入口就砍掉；不剪也对，只是慢。
6. 底部的 `assert` 把所有结果和 `itertools.combinations` 对拍，保证模板本身是对的。

## 3. 完整手算（Worked trace）

用括号生成 `n = 2` 看一遍 choose / explore / un-choose，以及「不能选」时发生了什么。下面的输出是真实运行结果：

```python
def trace_parens(n):
    path, answers = [], []
    calls = 0

    def go(opened, closed, depth):
        nonlocal calls
        calls += 1
        pad = "  " * depth
        if opened == n and closed == n:
            answers.append("".join(path))
            print(f"{pad}ANSWER {''.join(path)!r}")
            return
        if opened < n:
            path.append("(")
            print(f"{pad}choose '(' -> {''.join(path)!r}")
            go(opened + 1, closed, depth + 1)
            path.pop()
            print(f"{pad}undo   '(' -> {''.join(path)!r}")
        else:
            print(f"{pad}cannot open: budget of {n} used")
        if closed < opened:
            path.append(")")
            print(f"{pad}choose ')' -> {''.join(path)!r}")
            go(opened, closed + 1, depth + 1)
            path.pop()
            print(f"{pad}undo   ')' -> {''.join(path)!r}")
        else:
            print(f"{pad}cannot close: nothing open (closed={closed}, opened={opened})")

    go(0, 0, 0)
    print(f"answers={answers}  recursive calls={calls}  brute-force strings={2 ** (2 * n)}")
    return answers

assert trace_parens(2) == ["(())", "()()"]
```

```text
choose '(' -> '('
  choose '(' -> '(('
    cannot open: budget of 2 used
    choose ')' -> '(()'
      cannot open: budget of 2 used
      choose ')' -> '(())'
        ANSWER '(())'
      undo   ')' -> '(()'
    undo   ')' -> '(('
  undo   '(' -> '('
  choose ')' -> '()'
    choose '(' -> '()('
      cannot open: budget of 2 used
      choose ')' -> '()()'
        ANSWER '()()'
      undo   ')' -> '()('
    undo   '(' -> '()'
    cannot close: nothing open (closed=1, opened=1)
  undo   ')' -> '('
undo   '(' -> ''
cannot close: nothing open (closed=0, opened=0)
answers=['(())', '()()']  recursive calls=8  brute-force strings=16
```

怎么读这棵树：

- 缩进 = 递归深度。每次 `choose` 之后紧跟着它的子树，子树结束后出现同一缩进的 `undo`，`path` 回到 choose 之前的样子（例如 `undo ')' -> '(('` 之后回到上一层继续试别的选择）。
- `cannot close: nothing open` 就是剪枝：在 `''` 或 `'()'` 之后试图放 `)`，会让右括号多于左括号，整个子树被砍掉，**没有进入递归**。
- 一共 8 次递归调用就找到了全部 2 个答案；暴力「生成再过滤」要构造 16 个完整字符串。`n` 越大差距越大（`n = 10`：暴力要构造 1 048 576 个串，回溯只有 82 499 次递归调用，本机实测）。
- 注意没有任何地方「回溯」到某个旧状态再重新计算——回溯只是 `path.pop()` 加上函数返回。

## 4. 题目

```python
from collections import Counter
```

### 4.1 LC 22 · Generate Parentheses（Medium，频率 75）

```python
# solutions/22_generate_parentheses.py
def generate_parenthesis(n):
    out, path = [], []

    def go(opened, closed):
        if opened == n and closed == n:
            out.append("".join(path))
            return
        if opened < n:                       # may always open while we still have budget
            path.append("(")
            go(opened + 1, closed)
            path.pop()                       # un-choose
        if closed < opened:                  # may close only what is open: this prunes every invalid prefix
            path.append(")")
            go(opened, closed + 1)
            path.pop()

    go(0, 0)
    return out
```

- **一句话洞见**：任何时候，已放的 `)` 不能多于已放的 `(`，`(` 总数不能超过 `n`——这两条约束正好是两个 `if`，所有非法前缀在出生时就被剪掉。
- **复杂度**：输出规模是卡特兰数 `C(n) = (2n)! / (n!(n+1)!) ≈ 4^n / (n^1.5 · √π)`，时间 O(4^n / √n)（每个答案 O(n) 拷贝，总计 O(4^n · √n) 量级），递归栈空间 O(n)。
- 另一个视角：`S = "(" + A + ")" + B`（A、B 都是更小的合法串）给出 DP / 记忆化解法，输出相同；回溯版本更好写、也更好做成流式。

**资深追问**

- **规模 ×1000**：输出本身指数级（`n = 19` 已经是 17 亿个串），不可能放进列表。回答：改成**生成器**（`yield`），消费方边生成边处理；如果只要第 `k` 个串，用「前缀计数」直接跳转（ballot number 的 DP：已知前缀后剩余合法补全数），O(n²) 求第 `k` 个，不用枚举。
- **流式**：`def gen(n): ... yield "".join(path)` 内存 O(n)；调用方可以 `itertools.islice` 取前 1000 个。
- **内存**：返回列表是 O(C(n)·n)；生成器是 O(n)。
- **并发**：把前 3～4 个字符的所有合法前缀当作任务分给线程 / 进程（子树互相独立），各自输出到不同分片；合并时不需要去重。Python 里 CPU 密集用 `multiprocessing`，不是线程。
- **接口**：`n = 0` 返回 `[""]`（一个空串）而不是 `[]`；`n < 0` 抛 `ValueError`；顺序是否有要求（本实现是字典序，因为先试 `(`）。
- **测试**：卡特兰数计数（1, 1, 2, 5, 14, 42…）、无重复、每个输出用独立的校验函数（余额从不为负且最终为 0）、`n ≤ 5` 与「全部 2^(2n) 串再过滤」对拍。

### 4.2 LC 17 · Letter Combinations of a Phone Number（Medium，频率 67）

```python
# solutions/17_letter_combinations.py
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

def letter_combinations(digits):
    if not digits:
        return []                            # NOT [""]: LeetCode defines the empty input as "no combinations"
    out, path = [], []

    def go(i):
        if i == len(digits):
            out.append("".join(path))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            go(i + 1)
            path.pop()

    go(0)
    return out
```

- **一句话洞见**：每个数字是树的一层，每个字母是这一层的一个分支；没有约束，所以没有剪枝，只是纯枚举。它是理解「choose / explore / un-choose」的最小例子。
- **复杂度**：时间 O(4^n · n)（最多 4 个字母的键 `7`、`9`；n 是数字个数），空间 O(n) 递归栈（不含输出）。
- 对比 `itertools.product`：一行搞定，面试里可以先说「库里有，但我手写给你看」——面试官要的是你理解状态，不是调库。

**资深追问**

- **规模 ×1000**：输出指数级，同 4.1：生成器 + 分页；如果是自动补全 / 短信联想，不会真的枚举，而是用 trie 加词频（第 14 讲）。
- **流式**：数字逐个输入时，增量维护「当前所有候选前缀」并按需展开，类似 BFS 一层一层（`prefixes = [p + ch for p in prefixes for ch in PHONE[d]]`）。
- **内存**：BFS 版本一层要存全部前缀，DFS 版本只存一条路径。
- **并发**：第一位数字的 3～4 个字母各开一个任务。
- **接口**：空串返回 `[]`（不是 `[""]`——这是 LeetCode 的约定，务必先问）；输入里有 `0`、`1` 或非数字字符怎么办（抛异常 / 跳过 / 当作无字母）？键盘映射做成参数，方便换成 T9 之外的布局或多语言。
- **测试**：空串、单个数字、含 7 和 9 的 4 字母键、与 `itertools.product` 对拍、结果数量 = 各键字母数之积。

### 4.3 LC 79 · Word Search（Medium，频率 65）

```python
# solutions/79_word_search.py
def exist(board, word):
    rows, cols = len(board), len(board[0])
    if len(word) > rows * cols:
        return False
    have = Counter(ch for row in board for ch in row)
    if any(have[ch] < need for ch, need in Counter(word).items()):
        return False                                       # cheap global prune: letters are missing
    if have[word[0]] > have[word[-1]]:
        word = word[::-1]                                  # start the DFS from the rarer end

    def dfs(r, c, i):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        saved, board[r][c] = board[r][c], None             # mark visited (None never equals a letter)
        found = False
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, i + 1):
                found = True
                break
        board[r][c] = saved                                # un-choose BEFORE returning, on every path
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

- **一句话洞见**：在网格里做 DFS，每个格子**在当前路径上**只能用一次——用原地改成 `None` 来标记，递归返回前**还原**（un-choose）。
- **剪枝**：(1) 字母计数不够直接 `False`；(2) 从词两端中更稀有的一端开始搜，能把最坏情况的分支数大幅减少（例如 `aaaa…ab` 在全 `a` 的棋盘里，从 `b` 端开始会立刻失败）。
- **复杂度**：最坏 O(R·C·3^L)（L 是单词长度；第一步 4 个方向，之后每步最多 3 个，因为不能走回头路）；空间 O(L) 递归栈。
- 注意它**不是**第 06 讲的 flood fill：flood fill 的 `visited` 全局只增不减，这里的标记是**路径级**的，必须撤销。

**资深追问**

- **规模 ×1000**：棋盘大、查询词多（很多词）→ 不要一个词跑一遍，把所有词建成 trie，一次 DFS 同时匹配（下一讲 LC 212 Word Search II）。
- **流式**：查询词流式到达、棋盘固定：预处理「每个字母的位置列表」，从最稀有字母的位置出发。
- **内存**：原地标记 O(1) 额外空间 + 递归栈 O(L)。副作用：**函数运行期间棋盘被改动**，多线程同时读同一个棋盘会出错——并发场景要么每个线程拷贝，要么用位集 `visited` 作为参数传递（不可变）。
- **并发**：不同起点格子相互独立，可以并行；但必须各自持有 visited（不能共享原地标记）。
- **接口**：`L` 可能上千（递归深度超过 Python 默认 1000）→ 改显式栈；单词为空怎么办；是否允许斜向（8 连通）；区分大小写？
- **测试**：必须有「棋盘调用前后完全相同」的断言（我们的代码就有）、蛇形路径、重复使用同一格的反例（`ABCB`）、全相同字母的最坏用例、与「不可变 visited 集合」版本对拍。

### 4.4 LC 78 · Subsets（Medium，频率 64）；附 LC 90 与 LC 46

```python
# solutions/78_subsets.py
def subsets(nums):
    out, path = [], []

    def go(start):
        out.append(path[:])                   # every node of the recursion tree is an answer; COPY the path
        for i in range(start, len(nums)):
            path.append(nums[i])
            go(i + 1)                         # i + 1: each element used at most once, order fixed => no repeats
            path.pop()

    go(0)
    return out


def subsets_with_dup(nums):                   # LC 90: sort, then skip a value already tried at THIS level
    nums = sorted(nums)
    out, path = [], []

    def go(start):
        out.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            go(i + 1)
            path.pop()

    go(0)
    return out


def permutations_of(nums):                    # LC 46: "used" flags instead of a start index
    out, path, used = [], [], [False] * len(nums)

    def go():
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            go()
            path.pop()
            used[i] = False

    go()
    return out
```

- **一句话洞见**：递归树的**每个节点**（不只是叶子）都是一个答案；下一层从 `i + 1` 开始选，保证每个子集只以「升序」这一种顺序出现，所以不会重复。
- **复杂度**：2^n 个子集，每个拷贝 O(n)，总时间 O(n · 2^n)，空间 O(n) 递归栈。
- **三种变体一张表**（背这个）：

| 题 | 分支规则 | 去重 | 记录答案的时机 |
|---|---|---|---|
| 78 Subsets | `for i in range(start, n)` → `go(i+1)` | 无需 | 每个节点 |
| 90 Subsets II（有重复） | 同上 | 先排序，`i > start and nums[i] == nums[i-1]` 就跳过 | 每个节点 |
| 46 Permutations | `for i in range(n)`，跳过 `used[i]` | 无需（元素互不相同） | `len(path) == n` |

**资深追问**

- **规模 ×1000**：`n = 30` 就是 10 亿个子集，不能存。用生成器，或位掩码 `for mask in range(1 << n)`（每个子集 O(1) 增量更新：格雷码 Gray code 每次只翻转一位）。
- **流式**：元素一个个到达 → 已有子集集合 `S` 变成 `S ∪ {s + [x] for s in S}`（每来一个元素翻倍）；这是 BFS 视角的子集生成。
- **内存**：DFS 内存 O(n)；返回列表 O(n · 2^n)。
- **并发**：第一个元素「选 / 不选」两棵子树各自独立，可以任意深度拆分任务。
- **接口**：返回里的列表是**新的拷贝**还是共享引用（我们每次 `path[:]`；共享会导致调用方修改一个影响另一个）；输出顺序是否有保证；输入是否会被修改（我们没有，90 里是先 `sorted` 出新列表）。
- **测试**：`len == 2^n`、与 `itertools.combinations` 的并集对拍、带重复元素时去重正确（`[1,2,2]`）、空输入返回 `[[]]` 而不是 `[]`。

### 4.5 LC 51 · N-Queens（Hard，频率 62）；附 LC 52

```python
# solutions/51_n_queens.py
def solve_n_queens(n):
    boards, cols_of_row = [], []                 # cols_of_row[r] = column of the queen in row r
    cols, diag, anti = set(), set(), set()       # r - c is constant on "\" diagonals, r + c on "/" ones

    def go(r):
        if r == n:
            boards.append(["." * c + "Q" + "." * (n - c - 1) for c in cols_of_row])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                          # attacked: prune the whole subtree
            cols.add(c); diag.add(r - c); anti.add(r + c)
            cols_of_row.append(c)
            go(r + 1)
            cols_of_row.pop()
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)

    go(0)
    return boards


def total_n_queens(n):                            # LC 52: same search, three ints instead of three sets
    full = (1 << n) - 1

    def go(cols, diag, anti):
        if cols == full:
            return 1
        free = full & ~(cols | diag | anti)       # bit c set  <=>  column c is safe in this row
        count = 0
        while free:
            bit = free & -free                    # lowest safe column
            free ^= bit
            count += go(cols | bit, ((diag | bit) << 1) & full, (anti | bit) >> 1)
        return count

    return go(0, 0, 0)
```

- **一句话洞见**：一行放一个皇后（所以行冲突不可能发生，不需要检查）；列、"\\" 对角线（`r − c` 相同）、"/" 反对角线（`r + c` 相同）三种冲突用三个集合 O(1) 判断。每一行的候选就是「三个集合都没用过的列」。
- **复杂度**：最坏阶乘级，但剪枝后实际节点数小得多：`n = 8` 只有 92 个解，`n = 12` 有 14 200 个。空间 O(n)。
- **位运算版本（LC 52）**：用三个整数代替三个集合，`free & -free` 取最低位的可用列；对角线的下传是左移 / 右移一位。常数更小（本机 `n = 9` 实测约快 4 倍，其中集合版本还包含构造棋盘字符串的开销，仅供参考），而且体现「状态压缩」的资深加分。

**资深追问**

- **规模 ×1000**：只要**一个**解时，`n` 很大用构造法（O(n) 的显式公式，按 `n mod 6` 分情况）；要**全部**解数时，输出本身指数级，只能计数（LC 52）并利用左右对称：第一行只试左半部分再乘 2（奇数 `n` 的中间列单独处理）。
- **流式**：生成器 `yield` 每个解。
- **内存**：集合版 O(n)；位运算版 O(n) 个整数栈帧；输出所有棋盘是 O(解数 · n²)。
- **并发**：经典的并行例子——第一行的每一列各是一个独立任务，计数结果相加；没有共享状态。
- **接口**：返回棋盘字符串列表还是列位置列表（后者更紧凑）；`n = 2, 3` 无解返回 `[]`；`n = 0`？
- **测试**：OEIS A000170 的已知计数（1, 0, 0, 2, 10, 4, 40, 92, 352, 724），和「全排列再检查对角线」的暴力解对拍（我们 `n ≤ 7`）。

### 4.6 LC 37 · Sudoku Solver（Hard，频率 50）

```python
# solutions/37_sudoku_solver.py
def solve_sudoku(board):
    """board: 9x9 list of lists of '1'..'9' or '.'; solved IN PLACE; returns True if a solution exists."""
    rows, cols, boxes, empties = [0] * 9, [0] * 9, [0] * 9, []
    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                empties.append((r, c))
            else:
                bit = 1 << (int(board[r][c]) - 1)
                rows[r] |= bit; cols[c] |= bit; boxes[r // 3 * 3 + c // 3] |= bit

    def solve(k):                                  # empties[:k] are filled; choose the next cell among empties[k:]
        if k == len(empties):
            return True
        best, best_mask, best_count = k, 0, 10
        for i in range(k, len(empties)):           # MRV: the cell with the fewest candidates fails fastest
            r, c = empties[i]
            mask = ~(rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]) & 511
            count = bin(mask).count("1")
            if count < best_count:
                best, best_mask, best_count = i, mask, count
                if count <= 1:
                    break
        if best_count == 0:
            return False                           # dead end detected before branching
        empties[k], empties[best] = empties[best], empties[k]
        r, c = empties[k]
        b = r // 3 * 3 + c // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            board[r][c] = str(bit.bit_length())
            if solve(k + 1):
                return True
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
        board[r][c] = "."                          # un-choose the cell itself
        return False

    return solve(0)
```

- **一句话洞见**：不要按行从左到右填——每一步选**候选数最少的空格**（MRV，minimum remaining values）：候选只剩 1 个就是确定的（相当于免费的推理），剩 0 个就立刻判死。用 9 位的掩码表示行 / 列 / 宫已用的数字，`~(r | c | b) & 511` 就是候选集，`mask & -mask` 逐个取出。
- **复杂度**：理论上仍是指数级，但 MRV + 位运算让「普通 / 困难」谜题通常在毫秒级内解出（本讲测试里有一个著名的难题）。空间 O(81)。
- 这是「约束满足问题（CSP）」的标准解法；更一般的精确覆盖问题用 Algorithm X + Dancing Links（LC 题目标签里的 "Dancing Links"），面试里知道名字、能说出思想即可。

**资深追问**

- **规模 ×1000**：×1000 个谜题 → 每个独立求解，天然并行；单个谜题变大（16×16、25×25）→ MRV 仍然有效，最坏情况需要 Dancing Links 或把问题交给 SAT 求解器。
- **流式**：出题系统需要「是否唯一解」：搜索到第 2 个解就停（把 `solve` 改成计数并上限为 2）。
- **内存**：状态是 3 × 9 个整数 + 一个 81 个格子的列表。
- **并发**：对「第一个被选中的格子」的每个候选值开一个任务，各自拷贝一份状态。
- **接口**：原地修改 `board`（LeetCode 约定）；**无解时棋盘恢复原样**（我们的实现在失败回溯时会把格子还原为 `.`）；输入本身不合法（给定数字就冲突）时应该先用 LC 36 的校验拒绝，而不是让搜索白跑。
- **测试**：已知谜题的答案；任意一个已填满的合法棋盘随机挖洞再解，结果必须合法且保留原有数字（我们的测试就这样做）；无解输入（某格候选为 0）必须返回 `False` 且不死循环。

## 5. 常见 bug

1. **记录答案时没拷贝**：`out.append(path)`，最后 `out` 里全是空列表。写成 `path[:]`。
2. **忘记撤销**（尤其是 `used[]`、集合、计数器）：第一个分支的状态泄漏给第二个分支，结果偏少或偏多。检查方法：每个 `apply` 下面第三行必须有对应的 `undo`。
3. **提前 `return` 跳过撤销**：Word Search 里找到答案立刻 `return True` 会让棋盘永远带着 `None`；正确写法是先把结果存到变量、**还原**、再返回（上面的代码就是这样写的）。
4. **子集型用了 `i` 而不是 `i + 1`**：同一个元素被反复选，且会死循环（除非有 `remain` 约束，那是 LC 39 的写法）。
5. **去重条件写成 `i > 0`**：应该是 `i > start`——跳过的是**同一层**里重复的值，不是整个数组里重复的值，否则 `[1,2,2]` 会丢掉 `[2,2]`。
6. **对角线下标**：用数组而不是集合时，`r − c` 可能为负，要加偏移 `n − 1`。
7. **全局状态跨调用泄漏**：`out` / `path` 写成函数外的全局变量，第二次调用结果叠加在第一次上（LeetCode 会连续调用你的函数）。
8. **空输入的约定**：`subsets([]) == [[]]`、`generate_parenthesis(0) == [""]`，但 `letter_combinations("") == []`。这三个是不同的约定，不要凭感觉写。
9. **没有剪枝却以为是回溯**：先过滤再递归才叫剪枝；先递归到叶子再检查只是慢一点的暴力枚举。

## 6. 自测题

1. 回溯和普通 DFS 的区别是什么？
   <details><summary>答案</summary>回溯在递归返回时**撤销**对共享状态的修改，使每个兄弟分支从相同的现场开始；并且它的 visited 是「当前路径级」的而不是全局的。普通图 DFS 的 visited 全局只增不减，因为每个点只需要处理一次；回溯要枚举「所有路径」，同一个点会被不同路径多次经过。</details>
2. 为什么 `out.append(path)` 是错的？写出正确写法并解释。
   <details><summary>答案</summary>`path` 是同一个可变列表，递归结束时所有元素都被 pop 掉，`out` 里存的全是指向这个列表的引用，最后都是 `[]`。应写 `out.append(path[:])` 或 `list(path)`（拷贝，O(n)）。</details>
3. Subsets II（有重复元素）里，去重条件为什么是 `i > start and nums[i] == nums[i-1]`，不是 `i > 0`？
   <details><summary>答案</summary>排序后相同的值相邻。在**同一层**（同一个 `start` 下）选第二个相同的值会产生和选第一个相同的子树，所以跳过；但进入下一层后（`start` 变大），可以再选同一个值的下一个副本，这是 `[2,2]` 这样的合法子集的来源。`i > 0` 会把后者也跳过。</details>
4. 小编程：写出 LC 46 全排列的回溯，要求 `used` 数组正确撤销，并说明复杂度。
   <details><summary>答案</summary>见 4.4 的 `permutations_of`：`for i in range(n): if used[i]: continue; used[i] = True; path.append(nums[i]); go(); path.pop(); used[i] = False`。叶子 n! 个，每个拷贝 O(n)，总 O(n · n!)；空间 O(n)。</details>
5. N-Queens 里 `r − c` 和 `r + c` 分别对应哪条对角线？为什么能 O(1) 判冲突？
   <details><summary>答案</summary>同一条 "\\" 方向（左上到右下）的格子 `r − c` 相同；同一条 "/" 方向的格子 `r + c` 相同。两个皇后在同一条对角线上当且仅当其中一个值相同，所以把已放皇后的这两个值存进集合，新位置查集合即可。</details>
6. 资深追问：给你一个 `n = 25` 的括号生成请求，调用方想要「所有答案」，你怎么回应？
   <details><summary>答案</summary>先指出输出规模（卡特兰数 C(25) ≈ 4.8 × 10^12）不可能物化，问清真实需求：只要前 K 个 / 第 K 个 / 随机抽样 / 计数 / 校验某个串是否合法。对应方案：生成器 + 分页；用 ballot 计数 DP 的「第 K 个」直接构造；按前缀拆分任务并行；计数用 DP O(n²)。核心是把「回溯」换成「计数 / 排名」。</details>
7. 为什么 Sudoku 的 MRV 启发式有用？它改变了复杂度的上界吗？
   <details><summary>答案</summary>它不改变最坏上界（仍是指数级），但每步选择候选最少的格子：候选为 0 立即剪枝、为 1 时没有分支，大大减少实际访问的树节点。本质是「先处理最可能失败的决定，让错误尽早暴露」（fail-first）。</details>
