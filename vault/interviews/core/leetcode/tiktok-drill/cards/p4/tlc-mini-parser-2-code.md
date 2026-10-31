---
id: tlc-mini-parser-2-code
node: p4.mini-parser
type: qa
step: 2
---
## Q
**LC 385 迷你语法分析器**｜写出 Python 实现

字符串 `s`（`1 <= s.length <= 5 * 10^4`，只含数字、`[`、`]`、`-`、`,`，保证合法，数值在 `[-10^6, 10^6]`）表示整数的嵌套列表，返回 `NestedInteger`：`NestedInteger()` 是空列表，`NestedInteger(v)` 是整数，`add(x)` 追加元素。要求不因嵌套过深而递归爆栈。

## A
**思路。** 用正则切成记号，放进一个迭代器，所有递归层共享。`parse(tok)`：整数记号直接返回整数；`[` 就新建列表，用 `for nxt in tokens` 继续往后读，读到 `]` 结束，其余记号交给 `parse` 递归，结果加进列表。入口读第一个记号调用 `parse`。

```python
import re


def deserialize(s: str) -> NestedInteger:
    tokens = iter(re.findall(r"\[|\]|-?\d+", s))       # 切成 [  ]  整数 三种记号；共享一个迭代器当“读指针”

    def parse(tok: str) -> NestedInteger:              # 读完以 tok 开头的一个元素
        if tok != "[":
            return NestedInteger(int(tok))             # 整数：直接返回
        lst = NestedInteger()                          # 列表：继续读，直到对应的 ]
        for nxt in tokens:
            if nxt == "]":
                break
            lst.add(parse(nxt))                        # 子元素交给递归，它会用掉自己那一段记号
        return lst

    return parse(next(tokens))
```

运行（结果用嵌套 Python 列表表示）：`"324"` → `324`；`"[123,[456,[789]]]"` → `[123, [456, [789]]]`；`"[]"` → `[]`；`"[-1,[]]"` → `[-1, []]`；`"-5"` → `-5`；`"[[]]"` → `[[]]`。

**复杂度。** 时间 `O(n)`：切分一遍、每个记号读一次；空间 `O(n)`：记号列表，加上等于嵌套深度的递归栈。

**写法要点。** `re.findall` 的模式 `\[|\]|-?\d+` 同时解决了「多位数」和「负号」，逗号被自然丢掉；`iter(...)` 把列表变成一次性迭代器，`for nxt in tokens` 在递归里反复用同一个迭代器，每层消耗掉自己那一段，回到上一层时指针正好落在子元素之后，不需要传下标；`break` 在读到 `]` 时退出本层；整串只是一个整数时，`parse(next(tokens))` 直接走第一个分支，不需要特判。深度：`25000` 层嵌套会超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`，显式栈写法见追问卡。
