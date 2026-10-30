---
id: tlc-letter-combinations-of-a-phone-number-0-whole
node: p4.letter-combinations-of-a-phone-number
type: qa
---
## Q
**LC 17 电话号码的字母组合**｜Medium · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 14 次 · 最近 2026-09-17（CodeTop）

给一个只含数字 `2-9` 的字符串 `digits`，返回它能表示的所有字母组合，答案可以按任意顺序返回。数字到字母的映射和电话按键相同：`2` 对应 `abc`，`3` 对应 `def`，`4` 对应 `ghi`，`5` 对应 `jkl`，`6` 对应 `mno`，`7` 对应 `pqrs`，`8` 对应 `tuv`，`9` 对应 `wxyz`；`1` 不对应任何字母。`1 <= digits.length <= 4`，`digits[i]` 是 `['2', '9']` 中的一个数字。例：`digits = "23"` → `["ad","ae","af","bd","be","bf","cd","ce","cf"]`；`digits = "2"` → `["a","b","c"]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（backtracking）：`dfs(i)` 负责第 `i` 个数字，依次尝试它的每个字母——放进共享路径、递归下一位、再撤销；走到末尾就把路径拼成字符串收进答案。

**识别。** 「枚举所有组合，每一位从一个固定候选集里选一个」是回溯 / 笛卡尔积的信号；`digits.length <= 4` 说明答案规模不超过 `4^4 = 256`，指数级输出本身就是必然的，复杂度由答案大小决定，不是靠剪枝。近似但不同：LC 22 括号生成每一步有约束要剪枝，LC 78 子集是「选或不选」。

**推导。** 暴力思路是 `len(digits)` 层嵌套循环，每层遍历对应数字的字母；但层数不固定，写不出固定的嵌套 → 用递归代替，每一层递归处理一位。路径用一个共享的 `path` 列表，`append` 选择、递归、`pop` 撤销，避免每层都复制字符串；到叶子才 `"".join(path)`。迭代也可以：逐位把已有的前缀和新数字的每个字母配对。

```python
PHONE = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
         "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def letter_combinations(digits: str) -> list[str]:
    if not digits:                         # 空输入没有任何组合，返回 []（不是 [""]）
        return []
    ans: list[str] = []
    path: list[str] = []                   # 当前已选的字母，长度 == 当前处理到的位数

    def dfs(i: int) -> None:
        if i == len(digits):
            ans.append("".join(path))
            return
        for ch in PHONE[digits[i]]:
            path.append(ch)
            dfs(i + 1)
            path.pop()                     # 回溯：撤销选择

    dfs(0)
    return ans
```

运行：`"23"` → `['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']`；`"2"` → `['a', 'b', 'c']`；`""` → `[]`；`"7979"` 共 `256` 个组合。

**复杂度。** 时间 `O(n · 4^n)`：最多 `4^n` 个结果，每个拼接 `O(n)`；额外空间 `O(n)`（递归深度和 `path`），不含输出。

**易错点。**
- 忘了 `path.pop()`：路径只增不减，`"2"` 会得到 `['a', 'ab', 'abc']`（正确 `['a', 'b', 'c']`）。
- 收集答案时直接 `ans.append(path)` 而不 `join`：所有结果指向同一个列表，回溯结束后它被清空，`"23"` 的前三个结果都是 `[]`。
- 空串要返回 `[]`；不加判断会走到 `dfs(0)` 的叶子，返回 `[""]`。

**追问。**
- 不想递归：`ans = [""]`，每个数字做 `ans = [pre + ch for pre in ans for ch in PHONE[d]]`；或者 `product(*(PHONE[d] for d in digits))`，但后者隐藏了考点，面试里先写回溯。
- 数字含 `0` 或 `1`（没有字母）：跳过该位，或直接返回 `[]`，先和面试官确认语义。
- 要求结果是词典里的单词：把词典建成 Trie，回溯时沿 Trie 走，没有前缀就剪枝（T9 输入法联想）。

**同模式。** LC 22 括号生成、LC 78 子集、LC 46 全排列、LC 39 组合总和、LC 784 字母大小写全排列。
