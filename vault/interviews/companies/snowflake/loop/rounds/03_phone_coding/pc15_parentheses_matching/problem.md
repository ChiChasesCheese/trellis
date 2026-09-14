# pc15 · 括号匹配（栈）— 校验 / 补全 / 最长合法子串

> 电面题。Part 1 是一手报道的原题形态（"Parentheses Matching (Stack approach)"，无更多细节，按最常见的 LC 20 重建）；Part 2（LC 921）、Part 3（LC 32）是同一族"栈处理括号"题最常见的两个加深追问，**(reconstructed)**。

## 背景

一份 2026-03 的面经汇总把 "Parentheses Matching (Stack approach)" 列为电面例题之一，没有更多细节、没有其它来源交叉印证。这类标题几乎总是指 LC 20 Valid Parentheses 或它的变体；Part 1 按 LC 20 原题重建。真正有意思的地方在追问：**Part 1 是三种括号 `()[]{}`，Part 2/3 沿用它们各自原题（LC 921、LC 32）的约定，只处理小括号 `()`**——这个"括号种类突然变窄"本身就是一个容易漏掉的边界。

## 输入

- Part 1：`s: str`，只能含 `()[]{}` 六种字符。
- Part 2/3：`s: str`，**只能含 `(` 和 `)`**（LC 921、LC 32 的原始约定）。
- 出现其它字符 → 抛 `ValueError`。

## API 契约（英文签名）

```python
def is_valid(s: str) -> bool
def min_add_to_make_valid(s: str) -> tuple[int, str]
def longest_valid_substring(s: str) -> tuple[int, int]
```

## 规则

### Part 1 — 括号是否合法（LC 20 原题）

标准栈匹配：遇到左括号入栈，遇到右括号必须和栈顶的左括号种类匹配，否则不合法；扫描结束栈必须为空。

### Part 2 — 最少插入几个括号能合法，并给出一个结果（LC 921）**(reconstructed)**

只处理小括号。返回 `(最少插入次数, 一个合法结果字符串)`。**结果字符串按贪心构造**：碰到一个多余的 `)`（此时栈里没有未匹配的 `(`）就在它前面插入一个 `(`；扫描结束后栈里剩下的每个未匹配 `(` 都在字符串末尾补一个 `)`。

### Part 3 — 最长合法子串及其起始下标（LC 32）**(reconstructed)**

只处理小括号。返回 `(最长合法子串的长度, 起始下标)`。用"下标栈"经典解法：栈底放一个 `-1` 哨兵代表"当前这段合法子串开始之前的位置"；如果有多个并列最长的合法子串，**返回最靠左的那一个**（只在严格更长时才更新最优解）。空字符串或没有任何合法子串 → `(0, 0)`。

## Worked examples（全部由 `solution.py` 实际运行得出）

**例 1**（Part 1，三种括号）
```
is_valid("()")        -> True
is_valid("()[]{}")    -> True
is_valid("(]")        -> False   # 括号种类不匹配
is_valid("([)]")      -> False   # 交叉嵌套
is_valid("{[]}")      -> True
is_valid("")          -> True    # 空字符串合法
```

**例 2**（Part 2，LC 官方例子）
```
min_add_to_make_valid("())") -> (1, "()()")
min_add_to_make_valid("(((") -> (3, "((()))")
min_add_to_make_valid("()")  -> (0, "()")
min_add_to_make_valid(")(")  -> (2, "()()")   # 前面补一个"(" 给开头的")"，末尾补一个")" 给结尾的"("
```

**例 3**（Part 3，LC 官方例子）
```
longest_valid_substring("(()")     -> (2, 1)   # "()"，从下标1开始
longest_valid_substring(")()())")  -> (4, 1)   # "()()"，从下标1开始
longest_valid_substring("")        -> (0, 0)
longest_valid_substring("()(()")   -> (2, 0)   # 开头的 "()" 和结尾的 "()" 长度打平，取最靠左的
longest_valid_substring("()(())")  -> (6, 0)   # 整个字符串都合法
```

## `main()` 命令流

```
PART 1          PART 2          PART 3
()              ())             )()())
→ true          → 1             → 4 1
                  ()()
```

## 边界清单

- 空字符串：Part 1 合法（`True`）；Part 2 不需要插入（`(0, "")`）；Part 3 是 `(0, 0)`
- Part 1 三种括号互相交叉嵌套 `"([)]"` 不合法（栈顶匹配，不是"数量对上就行"）
- Part 1/2/3 出现非法字符（比如字母、Part 2/3 里出现方括号）→ `ValueError`
- Part 2：字符串已经合法时插入次数是 0，返回原字符串
- Part 2：全是 `(` 或全是 `)` 的极端情况
- Part 3：多个并列最长合法子串时取最靠左的（例 3 第 4 个例子）
- Part 3：没有任何合法子串（比如全是 `)`）→ `(0, 0)`
- 大规模：50 万字符要在 2 秒内跑完（纯栈/线性扫描，不能是 O(n²)）
- **line-driven 接口的限制**：`main()` 会跳过空行，所以内容为空字符串的输入行无法通过 stdin 表示——这类边界（`is_valid("")` 等）只在纯函数层面用 pytest 直接测试，不走 io 测试

## 追问

1. **为什么 Part 1 是三种括号，Part 2/3 却只有小括号？** 因为 Part 2、Part 3 各自对应的是 LC 921、LC 32 这两道独立的原题，它们的官方约定本来就只考虑小括号；把三种括号硬套进"最少插入"或"最长合法子串"会让"插入哪种括号""哪几个括号算一对"变得有歧义，所以延用各自原题的约定，在题面里显式提醒这个差异。
2. **Part 2 的结果字符串是唯一的吗？** 不唯一——只要插入次数等于最小值、结果合法即可，本题的贪心构造给出其中一种确定性方案（插入位置紧贴触发插入的字符），测试只验证这一种具体规则，不验证"所有可能的最优解"。
3. **Part 3 能不能用动态规划代替下标栈？** 可以，`dp[i]` = 以下标 `i` 结尾的最长合法子串长度，转移看 `s[i-dp[i-1]-1]` 是否是 `(`；两种解法复杂度相同，下标栈更省心因为它同时给出了起始下标。
4. **如果字符串里同时有小括号和需要校验嵌套的其它符号（比如 HTML 标签）？** 那是标签匹配的推广，本质相同（栈 + 匹配表），只是"括号种类"从字符换成了标签名字符串，需要用哈希表判断"闭合标签对应哪个开标签"。
5. **流式输入，字符一个个到来，要求实时判断"目前为止还有没有可能合法"？** 维护当前未匹配的 `(` 计数即可判断"目前不合法"（计数变负说明已经不可能合法，需要立刻报错/丢弃），但"最终是否合法"要等到流结束才能确定栈是否清空。

## 来源与置信度

- **LOW**：https://www.linkjob.ai/interview-questions/snowflake-software-engineer-interview/（2026-03-16），电面例题列出 "Parentheses Matching (Stack approach)"，无更多细节、无交叉印证，大概率是 LC 20 Valid Parentheses 或某个栈变体。见 `../../../../catalog/raw/coding_phone_onsite.md` #19。
- Part 2（LC 921 Minimum Add to Make Parentheses Valid）、Part 3（LC 32 Longest Valid Parentheses）未见一手报道，按栈处理括号类题目最常见的加深追问方向重建，已在题面标注 **(reconstructed)**。
- LC 20 / LC 921 / LC 32 官方题面：leetcode.com/problems/valid-parentheses/、.../minimum-add-to-make-parentheses-valid/、.../longest-valid-parentheses/。

## 考什么

栈的经典应用（匹配、补全、区间边界）· 三道题共享"栈"这个数据结构但状态设计完全不同（存字符 vs 存计数 vs 存下标）· 边界严谨性（字符集校验、并列结果的确定性 tie-break）。
