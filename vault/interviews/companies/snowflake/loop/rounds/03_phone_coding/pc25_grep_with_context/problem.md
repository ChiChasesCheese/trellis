# pc25 · Grep With Context Lines — 实现 `grep -C`：窗口合并、GNU 分组、流式 O(1) 内存

> 一手题面预览只给出函数签名与"像 `grep -C`"这一句；分组输出、`-B/-A`、流式版本均超出预览，
> **(reconstructed)**。

## 背景

TrueInterview 题单预览：`grep(lines, search_target, lines_around)`，行为像 `grep -C N`——返回
命中行以及前后各 `N` 行。这题本身不难，坑在**边界处理**：多个命中的上下文窗口重叠或相邻时要
**合并成一段连续区间**，不能重复输出同一行，且顺序必须是原文顺序。Part 2/3 把它往真实 `grep`
的方向继续推：分组之间的 `--` 分隔符、`-B/-A` 不对称、以及"日志是流不是列表"时如何不用无限内存。

## 输入

- Part 1：`lines: list[str]`、`search_target: str`（子串匹配，不是正则）、`lines_around: int
  >= 0`。
- Part 2：同上，把 `lines_around` 换成 `before: int >= 0` 和 `after: int >= 0`（分别对应
  `grep -B before -A after`）。
- Part 3：与 Part 1 相同的参数，但 `lines` 是一个**只能遍历一次、不可回看、不知道长度**的迭代器。

## API 契约（英文签名）

```python
def grep(lines: list[str], search_target: str, lines_around: int) -> list[str]
def grep_grouped(lines: list[str], search_target: str, before: int, after: int) -> list[str]
def grep_stream(lines: Iterable[str], search_target: str, lines_around: int) -> Iterator[str]
```

`lines_around < 0`（或 `before`/`after < 0`）→ `ValueError`。

## 规则

### Part 1 — 窗口合并（原题）

对每个命中行 `i`，把 `[i-lines_around, i+lines_around]`（截断到边界内）标记为"保留"；所有命中
的标记做**并集**（重叠或相邻窗口自然合并），最后按原始顺序输出所有被标记的行，**每行只输出一
次**（即使它同时落在两个命中的窗口里）。

### Part 2 — GNU 风格分组 + 不对称 `-B/-A` **(reconstructed)**

不再只有一个对称的 `lines_around`，而是 `before`（每个命中往前留几行）和 `after`（往后留几
行）分开配置。输出的"保留行"集合计算方式不变，只是每个命中的窗口变成
`[i-before, i+after]`。**新增**：如果两段被保留的连续区间之间有间隔（即中间有被跳过的行），
在它们之间插入一行字面量 `"--"`（GNU `grep -C`/`-A`/`-B` 的标准行为）；**第一段前面**和**最后一段
后面**都不加 `--`。

### Part 3 — 流式、O(lines_around) 辅助内存 **(reconstructed)**

`lines` 只能遍历一次。核心困难：**看到一行的那一刻还不知道它算不算命中的"后文"**——要等到再往
后多看 `lines_around` 行、确认期间没有新的命中需要更长的后文窗口，才能确定这一行到底要不要输
出。解法是维护一个大小固定为 `lines_around + 1` 的环形缓冲区（`collections.deque`），每读入一
行就把最老的一行"定案"（判断是否命中过而应该输出）并弹出；命中时就地把缓冲区里最近
`lines_around` 行标记为保留，并记一个"还需要把接下来 `lines_around` 行也标记为保留"的计数器。
辅助内存与 `lines_around` 成正比，与总行数无关。

## Worked examples（全部由 `solution.py` 实际运行得出）

```python
lines = ["a", "b", "ERR_x", "c", "d", "e", "ERR_y", "f", "g"]
```

**例 1**：`grep(lines, "ERR", 1) -> ["b", "ERR_x", "c", "e", "ERR_y", "f"]`
**例 2**：`grep(lines, "ERR", 0) -> ["ERR_x", "ERR_y"]`（只留命中行本身）
**例 3**：`grep(lines, "ERR", 5) -> lines` 本身全部（窗口越界截断到 0/末尾，恰好覆盖全表）
**例 4**：`grep_grouped(lines, "ERR", 1, 2) -> ["b","ERR_x","c","d","e","ERR_y","f","g"]`
（两个窗口 `[1,4]` 和 `[5,8]` 相邻贴合，合并成一段，没有 `--`）
**例 5**：`grep_grouped(lines, "ERR", 0, 0) -> ["ERR_x", "--", "ERR_y"]`（两段不相邻，中间插 `--`）
**例 6**：`list(grep_stream(iter(lines), "ERR", 1))` 与例 1 完全一致（500 组随机数据交叉验证于
`test_pc25.py`）

## `main()` 命令流

```
PART 1                         PART 2                              PART 3
N 9                            N 9                                 N 9
a                               a                                   a
b                               b                                   b
ERR_x                           ERR_x                                ERR_x
c                               c                                   c
d                               d                                   d
e                               e                                   e
ERR_y                           ERR_y                                ERR_y
f                               f                                   f
g                               g                                   g
Q ERR 1                         Q ERR 1 2                           Q ERR 1
→ b                            → b                                 → b
  ERR_x                          ERR_x                                ERR_x
  c                              c                                   c
  e                              d                                   e
  ERR_y                          e                                   ERR_y
  f                              ERR_y                                f
                                 f
                                 g
```

## 边界清单

- `lines_around = 0`（只留命中行本身，见例 2）
- `lines_around` 大到覆盖整个输入（截断到 `[0, len-1]`，见例 3）
- 完全没有命中 → 输出为空
- 两个命中的窗口重叠、相邻（合并成一段）、有间隔（Part 2 才插 `--`）
- 命中行本身也算在自己的窗口内（不会因为"是命中行"被排除在上下文之外）
- 负的 `lines_around` / `before` / `after` → `ValueError`
- Part 2 的 `--` 永远不出现在第一段之前或最后一段之后
- Part 3：连续多个命中挨得很近（后一个命中的"前文"窗口和前一个命中的"后文"窗口重叠）——流式版本
  必须和批量版本结果一致（见 `test_pc25.py` 的随机交叉验证）
- Part 3 辅助内存与 `lines_around` 成正比，不随输入行数增长（不能把整个输入攒成 list 再复用
  Part 1 的实现）
- 空输入 `lines = []` → 三个 Part 都返回空

## 追问

1. **`search_target` 换成正则表达式呢？** 只需要把 `search_target in line` 换成
   `re.search(pattern, line)`，窗口合并和流式缓冲区的逻辑完全不变。
2. **大小写不敏感匹配？** 同样是匹配谓词的替换，不影响架构。
3. **Part 3 的缓冲区大小为什么是 `lines_around + 1` 而不是 `2*lines_around + 1`？** 因为我们是
   "边读边定案最老的一行"：新读入的一行进队列后，队列头部那一行前面已经有它自己的 `lines_around`
   窗口信息在处理时被就地标记过（命中发生时直接回头标记缓冲区里已有的行），所以缓冲区只需要
   同时装得下"当前正在等待确认的最老一行"到"当前新读入的一行"之间的 `lines_around` 个新行，容量
   `lines_around + 1` 足够；如果只在读到命中时才回头标记而不是持续维护，容量分析要更小心（本题
   用的是"读到即标记"策略，因此更省)。
4. **能不能把 Part 2 的 `--` 分组和 Part 3 的流式结合？** 可以，把 Part 2 的"上一个保留行下标"
   判断挪进流式的 `_flush_one` 里，在两次真正 yield 之间检测索引是否连续即可，不需要额外内存。

## 来源与置信度

- **MED**：TrueInterview 同步的 Snowflake Algo 87 题清单第 25 项「Grep With Context Lines」，
  经 `kevin-2023-code/Tech-Interview-Questions`（聚合站，题面付费，仅预览的函数签名 + "像
  grep -C"一句可见），见 `../../../catalog/raw/github_repos.md` §2 第 25 行、§3 "pc25"。
- Part 2 的 `--` 分组、`-B/-A` 不对称，以及 Part 3 的流式 O(1) 版本均为重建，已标注
  **(reconstructed)**；行为对照的是真实 GNU `grep` 的 `-A/-B/-C` 语义。

## 考什么

S03（区间标记 + 合并，滑动窗口思维）· 流式算法设计（"延迟定案"模式：一行的命运要等看够后文才能
确定，用有界环形缓冲区而不是无界累积）· 边界截断与去重的仔细程度。
