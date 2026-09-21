# pc07 · Anagram Store：设计一个按 anagram 分组的存储结构

> 45 分钟第一轮编码题；热身函数 + Part 1/2 一手报道，Part 3 **(reconstructed)**。

## 背景

PracHub 的 Millennium 题单收录 "Design a data structure to store anagrams"（Technical Screen，2026-02-12）；同一份社区标签统计（StealthCoder）里 Valid Parentheses、Palindromic Substrings 也在 Millennium 的报道题目之列。本题把两者接成一题：先用 Valid Parentheses 热身（证明你能写栈），再进入设计题正文——存一批字符串，按"互为 anagram"分组，支持增删查与排行。

## API 契约（英文签名）

```python
def is_valid_parentheses(s: str) -> bool

def canonical_key_sorted(word: str) -> str
def canonical_key_counts(word: str) -> tuple[int, ...]   # 26-slot a-z count vector

class AnagramStore:
    def __init__(self, case_sensitive: bool = True) -> None: ...
    def add(self, word: str) -> None: ...
    def group_of(self, word: str) -> list[str]: ...
    def count(self, word: str) -> int: ...
    def remove(self, word: str) -> None: ...
    def most_common_group(self) -> list[str]: ...
    def top_k_groups(self, k: int) -> list[list[str]]: ...
```

- `s` 必须是只含 `()[]{}` 的 `str`；否则 `ValueError`。
- `word` 必须是 `str`；否则 `ValueError`。
- `canonical_key_counts` 只接受小写 `a-z`；其它字符（大写、数字、标点、非 ASCII）一律 `ValueError`。
- `case_sensitive` 必须是 `bool`；`k` 必须是正 `int`。

## 规则

### 热身 — Valid Parentheses（LC 20）

`is_valid_parentheses(s)`：用栈匹配 `()[]{}`。遇到左括号入栈；遇到右括号时栈顶必须是对应的左括号，否则不合法；扫完后栈必须清空。

### Part 1 — `AnagramStore.add / group_of / count`，两种分组键的对照

两个字符串互为 anagram，当且仅当它们的字符多重集合相同。有两种常见的"分组键"：

- `canonical_key_sorted(word)`：把字符排序拼回字符串，O(L log L)，对任意字符集（含 Unicode）都成立。
- `canonical_key_counts(word)`：26 位计数向量，O(L)，但只认小写 `a-z`。

`AnagramStore` 内部**统一用 `canonical_key_sorted`**（这样 Part 3 放开大小写/Unicode 限制时不用换实现）。`add(word)` 把 `word` 追加到它的分组（同一分组内保留插入顺序，同一个字符串可以出现多次，每次 `add` 都追加一个实例）。`group_of(word)` 返回 `word` 所在分组的全部词（插入顺序）；`word` 从未被加入过 → 返回 `[]`（不是错误，是正常的空结果）。`count(word)` 就是 `len(group_of(word))`。

### Part 2 — `remove` + `most_common_group`

`remove(word)`：从 `word` 所在分组里删除**恰好一个字面量等于 `word` 的实例**（不是"同组里任意一个词"——按字符串本身的身份删除，就像你只能退回你手上拿着的那一件货）。删除的是分组里插入顺序最靠前的那个匹配实例。如果这个具体字符串当前不在存储里（哪怕同组还有别的词），`ValueError`。

`most_common_group()`：返回成员数最多的分组（插入顺序）。空存储 → `[]`（不是错误）。并列时取**分组键（`canonical_key_sorted` 排序结果）字典序最小**的那组——这样结果永远不依赖插入顺序。

### Part 3 — 大小写/Unicode 策略 + 流式 top-k **(reconstructed)**

`AnagramStore(case_sensitive=False)`：分组键改用 `word.casefold()`（Unicode 正确的大小写折叠，比 `.lower()` 更通用）折叠后再排序；但分组里存的还是**原始大小写**的字符串，只是分组依据变了。

`top_k_groups(k)`：返回成员数最多的 `k` 个分组，按"成员数降序、分组键升序"排序（与 `most_common_group` 同一套并列规则）；分组总数不足 `k` 个时返回全部（不是错误）；`k <= 0` 或非 `int` → `ValueError`；空存储 → `[]`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**热身**
- `is_valid_parentheses("()[]{}") = True`
- `is_valid_parentheses("(]") = False`
- `is_valid_parentheses("([)]") = False`（顺序错误，不是简单的括号种类不匹配）
- `is_valid_parentheses("{[]}") = True`
- `is_valid_parentheses("") = True`（空串没有未匹配的括号）

**Part 1**（依次 `add`：`eat, tea, tan, ate, nat, bat`）
- `group_of("eat") = ["eat", "tea", "ate"]`，`count("eat") = 3`
- `group_of("bat") = ["bat"]`，`count("bat") = 1`
- `group_of("xyz") = []`（从未加入过）
- `canonical_key_sorted("eat") = "aet"`
- `canonical_key_counts("eat") = (1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)`（下标 0=a…4=e…19=t）

**Part 2**（在 Part 1 的六个词之上）
- `most_common_group() = ["eat", "tea", "ate"]`（3 个成员，比 `tan/nat`、`bat` 都多）
- `remove("eat")` 之后：`group_of("tea") = ["tea", "ate"]`，`most_common_group() = ["tea", "ate"]`

**Part 3**（`case_sensitive=False`，依次 `add`：`Eat, tea, TAN, ate, Nat, bat, listen, silent, enlist`）
- `group_of("eat") = ["Eat", "tea", "ate"]`（大小写不同也分到同一组，保留原始大小写）
- `top_k_groups(2) = [["Eat", "tea", "ate"], ["listen", "silent", "enlist"]]`（两组都是 3 个成员，并列按分组键字典序：`"aet"` < `"eilnst"`）

## `main()` 命令流

**Part 1**：`ADD <word>`（无输出）/ `GROUP <word>` → 分组内词空格拼接 / `COUNT <word>` → 整数。
**Part 2**：Part 1 的操作，另加 `REMOVE <word>`（无输出）/ `MOSTCOMMON` → 分组内词空格拼接。
**Part 3**：首行 `CASE SENSITIVE` 或 `CASE INSENSITIVE`，然后 `ADD <word>` / `TOPK <k>` → 各分组词空格拼接、分组间用 `|` 分隔。

```
PART 1
ADD eat
ADD tea
ADD tan
ADD ate
ADD nat
ADD bat
GROUP eat
COUNT eat
GROUP bat
→ eat tea ate
  3
  bat
```

## 边界清单

- 空存储上调用 `group_of` / `count` / `most_common_group` / `top_k_groups`：不抛异常，返回空结果
- `remove` 一个从未 `add` 过的词，或已经被删光的词 → `ValueError`；同一分组里还有别的词也不例外
- 同一个字符串被 `add` 两次：`group_of` 里出现两次；`remove` 一次只删一个实例，另一个还在
- `is_valid_parentheses` 含非括号字符 → `ValueError`；只有右括号（如 `")"`) → `False`；只有左括号（如 `"((("`) → `False`
- `canonical_key_counts` 遇到大写、数字、非 ASCII 字符 → `ValueError`；`canonical_key_sorted` 对任意 `str`（含 Unicode）都不报错
- `case_sensitive=False` 时，`"Eat"` 与 `"eat"` 同组，但 `group_of` 返回的字符串保留各自原始大小写
- `top_k_groups(k)`：`k` 大于现有分组总数 → 返回全部分组（不报错，不补空组）；`k` 非正数或非 `int` → `ValueError`
- `most_common_group` / `top_k_groups` 的并列必须按分组键字典序，不能按"先出现的分组"
- 性能：2 万次 `ADD`（随机小写词）之后一次 `TOPK`，本机端到端 < 2 s（`add` 均摊 O(L log L)，`top_k_groups` 是 O(G log G)，`G` 为分组数）

## 追问

1. **`canonical_key_sorted` 和 `canonical_key_counts` 该怎么选？** `counts` 是 O(L) 但被锁死在固定字母表（这里是小写 a-z）；`sorted` 是 O(L log L) 但对任意字符集通用。字母表固定且已知（比如只处理小写英文单词）时 `counts` 更快；一旦要支持大小写混合或 Unicode（Part 3），`counts` 的 26 位向量直接不够用，必须用 `sorted` 或等价的、支持任意字符的计数结构（比如 `Counter` 转成排序后的 `(char, count)` 元组）。
2. **为什么分组键要用元组/字符串而不是 `Counter` 本身？** `Counter`（`dict` 的子类）不可哈希，不能直接当 `dict` 的 key；要么转成排序字符串（本题做法），要么转成排序后的 `(char, count)` 元组。
3. **`AnagramStore` 的内存开销？** 每个词被存两次概念上的信息：原始字符串（在分组列表里）+ 隐式的分组键（`dict` 的 key，字符串本身也要占内存）；`N` 个长度 `L` 的词，大致是 `O(N * L)`（原始词）加上 `O(G * L)`（`G` 个分组键，`G <= N`）。
4. **`remove` 为什么按字面量而不是按分组任意删一个？** 如果存储代表的是"具体记录"（比如每条记录还挂着别的字段，这里简化成只有字符串本身），调用方通常是"删除我刚才插入的这一条"，不是"随便删同组里的一个"——按字面量删除是更贴近真实系统的语义，也让行为完全确定、可测试。

## 来源与置信度

- **HIGH**：PracHub `prachub.com/companies/millennium`（Technical Screen，2026-02-12）"Design a data structure to store anagrams"。
- **HIGH（社区标签统计，无逐字题面）**：StealthCoder Millennium 标签列表收录 Valid Parentheses（Easy）、Palindromic Substrings（Medium）——本题用 Valid Parentheses 做热身；Palindromic Substrings 不属于本族（anagram 分组），未纳入。
- Part 3（大小写/Unicode 策略、流式 top-k）未见一手报道，标 **(reconstructed)**：是"存储 + 分组查询"设计题最自然的追问方向（真实系统里输入不会永远是干净的小写英文）。

## 考什么

哈希分组键的设计权衡（O(L log L) 通用 vs O(L) 但字母表受限）· `dict` + `list` 组合实现"分组容器"的增删查改 · 排序稳定的并列打破规则（tie-break 必须写死，不能依赖迭代顺序）· 从"批量查询"扩展到"流式 top-k"时哪些状态可以增量维护、哪些必须重新排序。
