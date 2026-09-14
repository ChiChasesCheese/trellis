# pc07 · Word Search II（LC 212）— trie + 剪枝 DFS

> 60 分钟 senior 电面题的编码那一半。Part 1 是一手报道的原题；Part 2 是给出"具体走过哪些格子"的常见追问，**(reconstructed)**。

## 背景

2024-02 一位 Snowflake Senior Software Engineer 候选人的电面复盘（结果 Reject）：编码部分是 **LeetCode 212 Word Search II，未做改动**，候选人做出来了；同一 60 分钟槽的另一半是审计日志系统设计（见 `../../04_ood/` 或 `ood.md`，此处不涉及）。

真实难点不是"会不会写 trie"，而是三件事：**遍历到头之后要不要继续搜同一个词**（找到一次就该剪枝，否则大输入会重复扫描死分支）、**同一个格子在一条路径里不能用两次**、**边界一变就要把 trie 也跟着删**。

## 输入

- `board`：`R × C` 的小写字母网格（`'a'..'z'`），非空且每行等长。
- `words`：非空小写字母字符串列表。
- 合法路径：从任意格子出发，每步走到上下左右相邻且未在本条路径中用过的格子，拼出目标单词；**不允许对角线**。
- 空网格、行长不一致、非小写字母格子、空字符串或含非小写字母的单词 → 抛 `ValueError`。

## API 契约（英文签名）

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]
def find_words_with_paths(board: list[list[str]], words: list[str]) -> list[tuple[str, list[tuple[int, int]]]]
```

## 规则

### Part 1 — 找出所有能拼出的单词（LC 212 原题）

返回 `words` 中能在 `board` 上拼出的单词。**LC 本身不规定输出顺序**（只按集合判分）；本题把契约定死为**按字母升序排序**，便于测试和追问时复用。重复出现在 `words` 里的同一个词只算一次。

### Part 2 — 说出第一条路径 **(reconstructed)**

对每个找到的词，额外返回"第一条"路径（格子坐标 `(r, c)`，从起点到终点顺序排列）。"第一条"由两个固定的遍历顺序共同决定，写在下面，实现必须严格遵守：

1. **起点**按行优先（row-major）顺序尝试：`(0,0), (0,1), ..., (0,C-1), (1,0), ...`；
2. 从当前格子扩展时，**邻居按 上、下、左、右** 的固定顺序尝试：`(-1,0), (1,0), (0,-1), (0,1)`。

一个词一旦被第一次拼出，就把 trie 对应终止节点标记清除（不再记录第二条路径），并顺带把不再有子节点、也不是终止节点的死分支从 trie 上摘掉——这就是本题要考的"trie + 剪枝"：3 万词级别的 board 如果不剪枝，重复探测死分支会显著变慢。

返回值按词升序排序：`list[(word, path)]`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（LC 官方例 1）
```
board = [
  "oaan",
  "etae",
  "ihkr",
  "iflv",
]
words = ["oath", "pea", "eat", "rain"]

find_words            -> ["eat", "oath"]
find_words_with_paths -> [
  ("eat",  [(1,3), (1,2), (1,1)]),
  ("oath", [(0,0), (0,1), (1,1), (2,1)]),
]
```

**例 2**（LC 官方例 2：一个都找不到）
```
board = ["ab", "cd"]
words = ["abcb"]
find_words -> []
```

**例 3**（一个词的路径要在中途拐弯并重新经过相邻列）
```
board = [
  "abce",
  "sfcs",
  "adee",
]
words = ["abcced", "see", "abcb"]

find_words            -> ["abcced", "see"]
find_words_with_paths -> [
  ("abcced", [(0,0), (0,1), (0,2), (1,2), (2,2), (2,1)]),
  ("see",    [(1,3), (2,3), (2,2)]),
]
```

**例 4**（同一格子不能在一条路径里用两次：单格网格）
```
board = ["a"]
words = ["a", "aa"]
find_words -> ["a"]          # "aa" 需要用两次同一个格子，拼不出来
```

**例 5**（起点行优先决定"第一条路径"）
```
board = ["aa"]
words = ["aa"]
find_words_with_paths -> [("aa", [(0,0), (0,1)])]   # 从 (0,0) 出发，向右到 (0,1)
```

## `main()` 命令流

```
PART 1
4 4
oaan
etae
ihkr
iflv
W 4
oath
pea
eat
rain
→ eat oath
```

```
PART 2
1 2
aa
W 1
aa
→ aa 0,0 0,1
```
没有任何词被找到时，两个 part 都输出一行 `-`。

## 边界清单

- 网格为空 / 某一行长度与声明的 `C` 不一致 → `ValueError`
- 格子不是小写字母（大写、数字、多字符）→ `ValueError`
- 单词为空字符串或含非小写字母 → `ValueError`
- 单格网格，词长为 1 vs 词长 ≥ 2（后者必然找不到，因为不能重复用同一格）
- `words` 里出现重复词 → 只输出一次
- 一个词在网格里可能有多条路径，只需要"第一条"（起点行优先 + 邻居上下左右）
- 找不到任何词 → Part 1/2 都输出 `-`
- 大规模：12×12 board、3×10^4 个词（多数找不到）要在 2 秒内跑完 —— 剪枝是关键
- 目标词本身比网格总格子数还长 → 必然找不到，不应超时枚举

## 追问

1. **为什么找到一次就要把 trie 终止标记清掉？** 否则同一个词会被记录多次（我们只要第一条），而且不清掉、不剪枝的话，死分支会在后续每一次 DFS 调用里被重复访问，3 万词规模下明显变慢。
2. **能不能用 `visited` 矩阵代替原地改字符？** 可以，但原地把访问过的格子改成 `'#'`、退出时再还原是零额外内存的标准写法，本题采用后者。
3. **如果board允许对角线移动？** 把 `DIRS` 扩成 8 个方向即可，trie 剪枝逻辑不变。
4. **词表远大于 board 能拼出的组合数时怎么控制内存？** trie 只在存在的前缀上分支，实际节点数由 `words` 总字符数决定，与 board 大小无关；可以先用 board 上出现的字母集合过滤掉词表里包含 board 没有的字母的词，再建 trie。
5. **多线程/多进程能不能并行？** 可以按起点格子分片并行 DFS，但要注意 trie 的"找到一次就清掉终止标记"这一步在共享 trie 上必须加锁或改成每个分片私有 trie 再合并结果。

## 来源与置信度

- **HIGH（题号 + 未改动 + 结果）**：https://leetcode.com/discuss/interview-question/4727339/Snowflake-Senior-Software-Engineer-Phone-Screen/（2024-02-14，Senior Software Engineer，Reject）。编码部分明确是 LC 212 原题，候选人做出来了；同一 60 分钟槽另一半是审计日志系统设计。见 `../../../../catalog/raw/coding_phone_onsite.md` #1。
- Part 2（"给出具体路径"）未见一手报道，按 trie 类题目最常见的追问方向重建，已在题面标注 **(reconstructed)**。
- LC 212 官方题面：https://leetcode.com/problems/word-search-ii/description/

## 考什么

S08 LC 原题 + 复杂度再压一档（找到就剪枝，避免死分支重复扫描）· trie 上的回溯与状态清理（找到词后修改共享结构必须小心不要影响其它未完成的 DFS 分支）· 边界严谨性（网格校验、路径不可复用格子）。
