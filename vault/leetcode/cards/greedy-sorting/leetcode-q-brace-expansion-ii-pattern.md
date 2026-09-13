---
id: leetcode-q-brace-expansion-ii-pattern
node: greedy-sorting.sorting
type: qa
anki: 1789002116895
tags: [lc::1096, leetcode, pattern, recall]
---
## Q
如何用栈解析带优先级的表达式（如 Brace Expansion II 中 `,` 为并集、隐式连接为笛卡尔积拼接，且连接优先级高于并集）？

## A
维护两个栈：`stk` 存放当前的 set(str) 结果，`op` 存放待处理运算符（'+' 表示并集，'*' 表示连接，'{' 为分组标记）。扫描字符时：
- 遇到 `,`：先把栈顶所有 '*' 运算 pop 掉执行（保证连接优先级更高），再 push '+'。
- 遇到 `{`：若前一个字符是 `}` 或字母（即隐式连接），先 push '*'；再 push '{' 作为分组边界。
- 遇到 `}`：不断执行 op 直到遇到 '{'，然后把 '{' 弹出。
- 遇到普通字符：同样先判断是否需要隐式插入 '*'，再把单字符集合 push 进 stk。
- 最后清空 op 栈，结果排序去重（set 天然去重）。
执行运算 `ope()` 时：'+' 做集合 union（`stk[l] |= stk[r]`），'*' 做两个集合的笛卡尔积字符串拼接。

**Evidence**

```
def ope():
    l, r = len(stk) - 2, len(stk) - 1
    if op[-1] == '+':
        stk[l] |= stk[r]
    else:
        tmp = set()
        for left in stk[l]:
            for right in stk[r]:
                tmp.add(left + right)
        stk[l] = tmp
    op.pop(); stk.pop()

for i, ch in enumerate(expression):
    if ch == ',':
        while op and op[-1] == '*':
            ope()
        op.append('+')
    elif ch == '{':
        if i > 0 and (expression[i-1] == '}' or expression[i-1].isalpha()):
            op.append('*')
        op.append('{')
    elif ch == '}':
        while op and op[-1] != '{':
            ope()
        op.pop()
    else:
        if i > 0 and (expression[i-1] == '}' or expression[i-1].isalpha()):
            op.append('*')
        stk.append({ch})
while op:
    ope()
return sorted(stk[-1])
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1096%20-%20Brace%20Expansion%20II)
