---
id: tlc-mini-parser-4-followup
node: p4.mini-parser
type: qa
step: 4
---
## Q
**LC 385 迷你语法分析器**｜追问

面试官接着问：（1）嵌套 `25000` 层，递归会怎样，怎么改成不递归？（2）实现反过来的序列化，把 `NestedInteger` 写回字符串？（3）输入可能不合法（括号不配对、含空格），怎么检测？

## A
1. **深嵌套与显式栈**：递归深度等于括号嵌套层数，`25000` 层会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`。改成栈：栈顶始终是「正在往里填元素的那个列表」，`[` 压入新列表，整数加进栈顶，`]` 弹出栈顶并加进新的栈顶；栈空时弹出的就是最外层，即结果。整串只是一个整数的情形先单独处理，否则整数分支会访问空栈：

```python
import re


def deserialize_stack(s: str) -> NestedInteger:
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

2. **序列化**：递归拼接。整数返回 `str(v)`；列表返回 `"[" + ",".join(子元素的序列化) + "]"`。深度很大时同样要改成显式栈，否则会有和解析一样的递归深度问题。
3. **校验**：正则里加 `\s*` 吃掉空白；`]` 时栈已空且后面还有记号，或者扫描完栈不空，都说明括号不配对，抛 `ValueError`（递归版里对应：迭代器提前耗尽，或解析完还剩记号）。遇到不属于三类记号的字符，可以先用 `re.fullmatch(r"(?:\s*(?:\[|\]|,|-?\d+)\s*)*", s)` 整体校验。

**Python 提醒**：`re.findall` 在模式里有分组时返回的是分组内容而不是整个匹配；这里 `\[|\]|-?\d+` 没有括号分组，返回的就是完整记号。如果需要分组，改用 `re.finditer` 取 `m.group()`。`json.loads("[123,[456,[789]]]")` 一行得到嵌套 `list`，但这题考的就是手写解析，面试里不要绕开。
