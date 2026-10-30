---
id: tlc-letter-combinations-of-a-phone-number-4-followup
node: p4.letter-combinations-of-a-phone-number
type: qa
step: 4
---
## Q
**LC 17 电话号码的字母组合**｜追问

面试官接着问：（1）不用递归怎么写？（2）`itertools.product` 一行能解，面试里该怎么说？（3）输入可能含 `0`、`1` 怎么办？（4）结果必须是词典里的单词怎么办？

## A
1. **迭代**：从 `ans = [""]` 开始，对每个数字做一次扩展，每个已有前缀配上该数字的每个字母：

```python
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def letter_combinations_iter(digits: str) -> list[str]:
    if not digits:
        return []
    ans = [""]
    for d in digits:
        ans = [prefix + ch for prefix in ans for ch in PHONE[d]]
    return ans
```
   结果顺序与回溯完全一致（先固定前面的数字）。
2. **`product`**：`["".join(t) for t in product(*(PHONE[d] for d in digits))]` 结果相同，是标准库对笛卡尔积的直接封装。面试官想看的是回溯的结构（选择、递归、撤销），所以先写回溯，再说「标准库里有 `product`，等价且更短」。
3. **含 `0` / `1`**：它们没有字母。和面试官确认语义：跳过该位，还是视为无解返回 `[]`；实现上就是 `PHONE.get(d, "")` 加判断，或者先检查输入合法性。
4. **词典过滤**：先把词典建成 Trie（前缀树），回溯时同步沿 Trie 走，没有对应子结点就剪枝，不再展开；比生成全部 `4^n` 个再过滤省得多，这就是 T9 输入法联想的做法。

**Python 提醒**：`product(*lists)` 是惰性迭代器，需要 `list(...)` 才能多次遍历；字符串拼接 `prefix + ch` 每次生成新字符串，在长度上限只有 `4` 时无所谓，位数很多时用 `path` 列表加 `join`。
