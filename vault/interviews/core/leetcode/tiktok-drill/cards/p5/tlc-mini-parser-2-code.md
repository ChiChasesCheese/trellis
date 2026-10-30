---
id: tlc-mini-parser-2-code
node: p5.mini-parser
type: qa
step: 2
---
## Q
**LC 385 迷你语法分析器**｜写出 Python 实现

字符串 `s`（`1 <= s.length <= 5 * 10^4`，只含数字、`[`、`]`、`-`、`,`，保证合法，数值在 `[-10^6, 10^6]`）表示整数的嵌套列表，返回 `NestedInteger`：`NestedInteger()` 是空列表，`NestedInteger(v)` 是整数，`add(x)` 追加元素。要求不因嵌套过深而递归爆栈。

## A
**思路。** 整串不以 `[` 开头就是单个整数。否则用正则切成记号，栈里放「正在填写的列表」：`[` 压入新列表；整数加进栈顶；`]` 弹出栈顶，栈空则返回它，否则加进新的栈顶。

```python
import re


def deserialize(s: str) -> NestedInteger:
    if s[0] != "[":                                    # 整个串就是一个整数
        return NestedInteger(int(s))
    stack: list[NestedInteger] = []
    for tok in re.findall(r"\[|\]|-?\d+", s):          # 切成 [  ]  整数 三种记号
        if tok == "[":
            stack.append(NestedInteger())              # 开一个新列表
        elif tok == "]":
            done = stack.pop()
            if not stack:                              # 最外层闭合：解析完成
                return done
            stack[-1].add(done)                        # 否则挂到父列表上
        else:
            stack[-1].add(NestedInteger(int(tok)))
    raise ValueError(s)
```

运行（结果用嵌套 Python 列表表示）：`"324"` → `324`；`"[123,[456,[789]]]"` → `[123, [456, [789]]]`；`"[]"` → `[]`；`"[-1,[]]"` → `[-1, []]`；`"-5"` → `-5`；`"[[]]"` → `[[]]`；`25000` 层嵌套正常返回。

**复杂度。** 时间 `O(n)`：切分一遍、每个记号处理一次；空间 `O(n)`：记号列表和栈。

**写法要点。** `re.findall` 的模式 `\[|\]|-?\d+` 同时解决了「多位数」和「负号」，逗号被自然丢掉；`stack[-1]` 取栈顶而不弹出；最后的 `raise ValueError` 让函数在非法输入时显式失败，而不是悄悄返回 `None`（类型标注是 `NestedInteger`）。
