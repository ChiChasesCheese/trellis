# pc07 · Anagram Store：练的是"分组键的选择与并列规则的写死"

> [!tldr]
> - 这题考的是：能不能把"互为 anagram"翻译成一个可哈希的分组键，并且把"并列时选谁"想清楚、写死
> - 三步套路：先证明会写栈（热身）→ 定好分组键，跑通 add/group_of/count → 在同一套 dict 上叠加 remove、排行、策略开关
> - 最值得带走的一个模式：**"按某种等价关系分组"的题，核心动作永远是"把等价类映射成一个可哈希的 key"，剩下的都是在这个 `dict[key, list]` 上做增删查改**

## 1. 题目在说什么（人话版）

热身：给一个只含 `()[]{}` 的字符串，判断括号是不是配对合法（LC 20）。正文：设计一个存字符串的结构，支持按"互为 anagram"分组——加词、查某个词所在的组、数组内有几个词、删掉一个词、找出成员最多的组、大小写不敏感时怎么分、按成员数取 top-k。

```
add("eat"); add("tea"); add("tan"); add("ate"); add("nat"); add("bat")
group_of("eat") -> ["eat", "tea", "ate"]     # 三个词字符多重集合相同
most_common_group() -> ["eat", "tea", "ate"]  # 3 个成员，比 tan/nat（2 个）、bat（1 个）都多
```

## 2. 读题：把文字变成模型

- **实体**：一个"分组"（同一个字符多重集合的所有词）；一个"分组键"（能唯一代表这个多重集合、且可哈希的值）。
- **输入长什么样**：一个个字符串（词），逐个 `add` 进来。
- **输出要什么**：某个词所在分组的全部成员（插入顺序）、分组大小、成员最多的分组、前 k 大的分组。
- **状态**：`dict[分组键, list[词]]`——键决定"谁和谁同组"，值的列表顺序决定"组内输出顺序"。
- **一句话建模**：这是一个**按等价关系（互为 anagram）分组**的计数问题，和"按 user_id 分组求和"是同一个骨架，只是分组键从"直接给的字段"变成了"需要计算出来的字符排序结果"。

> [!note] 为什么选 `dict[str, list[str]]`
> 分组键必须可哈希——`Counter`（`dict` 子类）本身不行，要么排序成字符串（通用，O(L log L)），要么转成固定长度的计数元组（O(L)，但锁死字母表）。本题两者都写，用来讲清楚这个权衡；`AnagramStore` 内部选排序字符串，因为它对大小写策略、Unicode 都不用换实现。

## 3. 下笔顺序（面试里就按这个顺序敲）

1. **骨架先行**：热身函数独立写完（栈 + 括号匹配表），先过样例。
2. **分组键最小可用**：`canonical_key_sorted(word) = "".join(sorted(word))`。立刻验证 `"eat"` 和 `"tea"` 键相同。
3. **`add`/`group_of`/`count`**：`dict.setdefault(key, []).append(word)`；`group_of` 直接查表，未命中返回 `[]`（不是异常）。
4. **`remove`**：从对应分组的 list 里删一个"字面量匹配"的元素（`list.remove`），组空了就把这个 key 从 dict 里删掉，避免"空分组"污染后续的 `most_common_group`。
5. **`most_common_group`/`top_k_groups`**：`sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))`——一行代码同时解决"按大小降序"和"并列按键升序"。
6. **收尾**：`case_sensitive` 开关（`casefold()` 后再排序，但存原始大小写）、输入校验（非 `str`、`k` 非正整数）。

## 4. 代码怎么组织

```
is_valid_parentheses(s)                  # 热身，独立函数
canonical_key_sorted(word)               # 分组键 v1：通用
canonical_key_counts(word)               # 分组键 v2：O(L) 但限 a-z（对照用）
AnagramStore
  ._key(word)                            # 按 case_sensitive 策略折叠后调 canonical_key_sorted
  .add / .group_of / .count              # 基础三件套
  .remove                                # 按字面量身份删
  .most_common_group / .top_k_groups     # 复用同一条排序 key
part1..part3 / main
```
`_key` 是唯一"决定谁和谁同组"的地方，大小写策略改动只用碰这一个函数；`most_common_group` 和 `top_k_groups` 共享同一条排序 key，避免两处并列规则写岔。

## 5. 核心代码（骨架，≤ 40 行，带注释）

```python
def canonical_key_sorted(word: str) -> str:
    return "".join(sorted(word))          # O(L log L)，任意字符集

class AnagramStore:
    def __init__(self, case_sensitive: bool = True) -> None:
        self.case_sensitive = case_sensitive
        self._groups: dict[str, list[str]] = {}

    def _key(self, word: str) -> str:
        folded = word if self.case_sensitive else word.casefold()
        return canonical_key_sorted(folded)

    def add(self, word: str) -> None:
        self._groups.setdefault(self._key(word), []).append(word)

    def most_common_group(self) -> list[str]:
        if not self._groups:
            return []
        best = min(self._groups, key=lambda k: (-len(self._groups[k]), k))  # 并列取键最小
        return list(self._groups[best])
```

## 6. Talking through it in the interview

- Before starting: "I'll represent each anagram group as a dict keyed by the sorted characters of the word — that's O(L log L) but works for any alphabet, versus a 26-slot count vector which is O(L) but only valid for lowercase a-z."
- Writing `remove`: "I'm deleting by literal string identity within the group, not any member with the same key — that matches how a caller would expect to remove the exact record they inserted."
- Writing the tie-break: "When two groups are the same size, I break the tie by the group's own key in lexicographic order, so the answer never depends on insertion order."
- On delivery: "The worked examples pass; if time allows, I'd add the case-insensitive policy and a streaming top-k on top of the same dict."

## 7. 常见跑偏（方法层面，3 条）

- 分组键选了 `Counter` 本身当 dict 的 key——`Counter` 不可哈希，得先转成排序字符串或排序后的元组。
- `remove` 直接删"同组里随便一个"——如果调用方期望删除的是它插入的那个具体实例，行为会和预期不一致，而且不可测试（结果依赖实现的内部遍历顺序）。
- 并列规则想到哪写到哪（这次按插入顺序，下次按词本身字典序）——`most_common_group` 和 `top_k_groups` 必须共用同一条 tie-break key，否则两个查询会给出不一致的"第一名"。

## 8. 同族题 / 延伸

- 和 pc01（按 id 分组聚合）是同一个"分组键 → dict[key, 累加值/列表]"骨架，只是这里的"键"需要现算（排序字符）而不是直接给的字段。
- 练习命令：`python3 loop/mock.py start pc07`
