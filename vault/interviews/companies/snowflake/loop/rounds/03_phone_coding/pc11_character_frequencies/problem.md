# pc11 · 字符频率统计 — 跨字符串 / 跨任意深度嵌套列表

> 电面里常见的"暖场题"（正式题之前的一道 Easy）。Part 1 是一手报道的原题形态；Part 2、Part 3 是同一站点报的"嵌套列表"变体和最常见的 top-k 追问，**(reconstructed)**。

## 背景

fastprep.io 收录了两道 Snowflake 电面 Easy 题：「统计多个字符串里每个字符出现的次数」和「统计任意深度嵌套字符串列表里每个字符出现的次数」，都标注为 Phone Screen、Array/Hash-Table，最近一次报告 2026-06。结合同来源反复出现的"一场电面两道题"格式（见 pc05 背景），这类题大概率是正式题之前的暖场题。

真正的坑不在"用哈希表计数"，而在：**统计的是所有字符（含空格、标点），不是只统计字母**；**排序的 tie-break 必须写死**（次数相同按字符本身升序）；以及 Part 2 追问里**任意深度嵌套列表不能用递归展开**——嵌套到几万层会撞到 Python 的递归深度限制，必须用显式栈迭代。

## 输入

- Part 1：`strings: list[str]`，扁平的字符串列表。
- Part 2 / Part 3：`data`，任意深度嵌套的列表，叶子是字符串，容器是 `list`（可以嵌套 `list` 套 `list`）。
- 统计单位是**单个字符**（Unicode code point），空格、标点、重复字符都算数。
- 非字符串叶子、非 `list` 容器、Part 1 收到嵌套结构 → 抛 `ValueError`。

## API 契约（英文签名）

```python
def char_frequencies(strings: list[str]) -> list[tuple[str, int]]
def char_frequencies_nested(data: list) -> list[tuple[str, int]]
def top_k_chars(data: list, k: int) -> list[tuple[str, int]]
```

## 规则

### Part 1 — 扁平字符串列表的字符频率

统计 `strings` 里所有字符串拼接起来后每个字符出现的次数，按 **次数降序、次数相同时字符升序** 排序返回 `(char, count)` 列表。

### Part 2 — 任意深度嵌套列表 **(reconstructed)**

输入变成任意深度嵌套的列表（叶子仍是字符串）。**必须用显式栈迭代展开，不能用递归**——嵌套深度可能有几万层，递归会撞 `RecursionError`。展开后统计规则、排序规则与 Part 1 完全一致。

### Part 3 — Top-K，打平的都要 **(reconstructed)**

在 Part 2 的排序结果里取前 `k` 个，但**如果第 `k` 名和后面的字符次数相同，要把并列的全部带上**（所以返回长度可能大于 `k`）。`k = 0` → 空列表；`k` 超过不同字符总数 → 返回全部。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（基本计数 + 排序）
```
char_frequencies(["abb", "bcc"]) -> [("b", 3), ("c", 2), ("a", 1)]
```

**例 2**（空格和标点也要算，不是只统计字母）
```
char_frequencies(["a a!", "a!"]) -> [("a", 3), ("!", 2), (" ", 1)]
```

**例 3**（任意深度嵌套）
```
data = ["ab", ["cd", ["ef", "gh"]], "ij"]
char_frequencies_nested(data) -> [("a",1), ("b",1), ("c",1), ("d",1), ("e",1),
                                   ("f",1), ("g",1), ("h",1), ("i",1), ("j",1)]
```

**例 4**（top-k 打平要全带上）
```
top_k_chars(["aabbcc"], 1) -> [("a", 2), ("b", 2), ("c", 2)]   # 第1名和第2、3名并列，全带上
top_k_chars(["aabbbcc"], 2) -> [("b", 3), ("a", 2), ("c", 2)]  # 第2名和第3名并列
top_k_chars(["ab"], 10) -> [("a", 1), ("b", 1)]                 # k 超过总数，返回全部
top_k_chars(["aabbcc"], 0) -> []
```

**例 5**（深度嵌套不炸栈：2 万层嵌套的单字符串，展开后仍能正确统计出 1 个字符）
```
data = [[[...["x"]...]]]   # 20000 层
char_frequencies_nested(data) -> [("x", 1)]
```

## `main()` 命令流

Part 1/2/3 都输出 `char count` 每行一条（次数降序、字符升序），空结果输出一行 `-`。Part 2/3 的嵌套结构用一行类 JSON 的列表字面量表示（用手写的显式栈扫描器解析，**不用 `ast.literal_eval` / `json.loads`**——这两者自己也是递归实现，嵌套几千层就先于我们的代码报 `RecursionError`/`SyntaxError`，会让"迭代展开"这个考点在 IO 层面失去意义）：

```
PART 1                PART 2                          PART 3
N 2                   ["ab", ["cd"], "ab"]             K 1
abb                   → a 2                            ["aabbcc"]
bcc                     b 2                             → a 2
→ b 3                   c 1                               b 2
  c 2                    d 1                               c 2
  a 1
```

## 边界清单

- 空字符串列表 / 空嵌套列表 → 输出 `-`
- 字符串里的空格、标点、重复字符都要算（例 2）
- Part 1 收到嵌套 `list`（而不是字符串）→ `ValueError`（应该走 Part 2 的 API）
- Part 2/3 顶层不是 `list` → `ValueError`；叶子既不是 `str` 也不是 `list` → `ValueError`
- 极深嵌套（测试用 2 万层）不能递归展开，必须用显式栈
- Top-k 边界：`k = 0`、`k` 超过不同字符总数、恰好打平在截断点上（例 4 两种打平场景都要测）
- Unicode 多字节字符（如中文、emoji）当作单个 code point 统计
- line-driven 接口的限制：`main()` 会跳过空行，所以内容为空白/换行的字符串元素无法通过 stdin 表示——这类边界只在纯函数层面用 pytest 直接测试，不走 io 测试

## 追问

1. **为什么不能用递归展开嵌套列表？** Python 默认递归深度限制约 1000；嵌套列表来自不受信任的输入（比如日志里递归的 JSON 结构）时，几万层嵌套会直接抛 `RecursionError`。显式栈（`list` 当栈、`iter()` 当帧）把"当前正在遍历哪一层的哪个位置"存在栈里，不占用 Python 调用栈。
2. **能不能只统计字母，忽略大小写？** 那是产品需求问题，不是算法问题——本题按"统计所有字符、区分大小写"定契约；如果要求忽略大小写，只需要在计数前对每个字符调用 `.lower()`。
3. **Top-k 打平之后还要不要保证总长度可控？** 不保证——如果所有字符次数相同，`top_k_chars(data, 1)` 会返回全部不同字符，这是题目要求"打平的都要"的直接后果，需要在追问里明确说清楚这个退化情况。
4. **流式输入，字符串不断到来？** 维护一个运行中的计数哈希表即可增量更新；重新排序/取 top-k 时如果数据量大，可以用堆维护当前 top-k 候选，只有当次数变化触及堆顶时才重新调整。
5. **能不能用 `collections.Counter`？** 可以，`Counter.most_common()` 不保证同次数时的字符顺序是升序，仍需要在其基础上按 `(-count, char)` 显式重新排序。

## 来源与置信度

- **MED（结构化来源，暖场题）**：https://www.fastprep.io/problems/snowflake-character-frequency-across-strings 与 https://www.fastprep.io/problems/snowflake-character-frequency-across-nested-lists，均为 Easy / Array-Hash-Table / Phone Screen，最近报告 2026-06。见 `../../../../catalog/raw/coding_phone_onsite.md` #6。
- Part 3（top-k 打平全带上）未见一手报道，按计数排序类暖场题最常见的追问方向重建，已在题面标注 **(reconstructed)**。

## 考什么

S06（计数哈希 + 排序 tie-break，与滑窗/事件流题共享"确定性排序契约"的考法）· 迭代展开任意深度结构、避免递归深度限制 · 边界处理的严谨性（空输入、类型校验）。
