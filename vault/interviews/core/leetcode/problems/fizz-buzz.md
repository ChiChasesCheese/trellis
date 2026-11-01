---
slug: fizz-buzz
---
## Q
**LC 412 Fizz Buzz（Fizz Buzz）**｜Easy

给你一个整数 `n`，返回一个字符串数组 `answer`（下标从 1 开始），其中：如果 `i` 同时是 3 和 5 的倍数，`answer[i] == "FizzBuzz"`；如果 `i` 是 3 的倍数，`answer[i] == "Fizz"`；如果 `i` 是 5 的倍数，`answer[i] == "Buzz"`；如果上述条件全不满足，`answer[i]` 是 `i` 的字符串形式。`1 <= n <= 10^4`。例：`n = 3` → `["1","2","Fizz"]`；`n = 5` → `["1","2","Fizz","4","Buzz"]`；`n = 15` → 最后一项是 `"FizzBuzz"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 模拟 + 字符串拼接：把「是 3 的倍数」「是 5 的倍数」两个独立条件各自贡献一段文字。

**一句话。** 对每个 `i`，3 的倍数拼上 `"Fizz"`，5 的倍数拼上 `"Buzz"`；拼出来是空串就用数字本身。

**识别。** 规则互相独立、`15` 的倍数要同时满足两个：拼接比 `if/elif` 链少写一个 `15` 的分支。面试里它是热身，重点是干净且好扩展。

**推导。** `if i % 15 == 0 ... elif i % 3 == 0 ... elif i % 5 == 0` 对两条规则够用，但再加一条规则（7 的倍数 `"Jazz"`）分支数翻倍。拼接写法下，每条规则独立，新规则只加一项。

```python
def fizz_buzz(n: int) -> list[str]:
    ans: list[str] = []
    for i in range(1, n + 1):
        word = ("Fizz" if i % 3 == 0 else "") + ("Buzz" if i % 5 == 0 else "")   # 15 的倍数自然拼成 FizzBuzz
        ans.append(word or str(i))                # 没命中任何规则就是数字本身
    return ans
```

运行：`3` → `['1', '2', 'Fizz']`，`5` → `['1', '2', 'Fizz', '4', 'Buzz']`，`15` 的最后一项 → `'FizzBuzz'`，`1` → `['1']`。

**复杂度。** 时间 `O(n)`，空间 `O(1)` 额外（不计输出）。

**拓展优化。**
- 面试常追问「再加规则」：把规则放进有序表，`n = 21` 加上 `(7, "Jazz")` 只改数据不改逻辑。

```python
def fizz_buzz_rules(n: int, rules: list[tuple[int, str]]) -> list[str]:
    # 规则放进表里：新增「7 -> Jazz」只改数据，不改逻辑；规则顺序决定拼接顺序
    return ["".join(word for d, word in rules if i % d == 0) or str(i) for i in range(1, n + 1)]
```

例：`rules = [(3, "Fizz"), (5, "Buzz"), (7, "Jazz")]`，`n = 21` 的最后八项是 `['Jazz', 'FizzBuzz', '16', '17', 'Fizz', '19', 'Buzz', 'FizzJazz']`。

**易错点。**
- `if i % 3 == 0 ... elif i % 5 == 0 ... elif i % 15 == 0`：`15` 被前面的 `3` 的分支截走，`n = 15` 最后一项成了 `"Fizz"`，正确 `"FizzBuzz"`。`15` 的分支必须放在最前，或者用拼接。
- 规则表顺序放反：`[(5, "Buzz"), (3, "Fizz")]` 时 `15` 得到 `"BuzzFizz"`，顺序由规则表决定。
- 下标从 0 开始（`range(n)`）：第一项成了 `"FizzBuzz"`（`0` 是所有数的倍数），正确是 `"1"`。

**同模式。** LC 12 整数转罗马数字、LC 13 罗马数字转整数、LC 168 Excel 表列名称、LC 17 电话号码的字母组合。
