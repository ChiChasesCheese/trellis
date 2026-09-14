---
id: cc-input-gram-parse-error-policy
node: input.grammar
type: qa
---
## Q
One rule in the input is syntactically invalid. Should the parser skip it, or fail?

## A
**The parser raises; the caller decides.**

```python
try:
    rules.append(compile_rule(text))
except ValueError:
    pass          # this stream's policy: an unparsable rule is ignored
```

A parser that silently returns "always false" for a bad rule hides the error from every caller and makes the same function untestable. Raising keeps the parser honest and lets one call site implement the stream's stated policy — usually "a rule that fails to parse is ignored", occasionally "reject the whole input". The policy belongs where the statement puts it, not inside the grammar.

## Q zh
输入里有一条规则语法非法。解析器应该跳过它，还是失败？

## A zh
**解析器抛错；调用方决定。**

```python
try:
    rules.append(compile_rule(text))
except ValueError:
    pass          # this stream's policy: an unparsable rule is ignored
```

对坏规则默默返回"恒假"的解析器，会把错误对所有调用方隐藏起来，也让这个函数无法测试。抛错让解析器保持诚实，并让唯一的调用点去实现题面规定的策略 —— 通常是「解析失败的规则被忽略」，偶尔是「整份输入作废」。策略应放在题面指定的位置，而不是塞进文法里。
