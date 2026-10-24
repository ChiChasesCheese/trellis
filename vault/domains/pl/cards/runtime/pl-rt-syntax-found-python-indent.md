---
id: pl-rt-syntax-found-python-indent
node: runtime.syntax-parsing
type: qa
step: 4
---
## Q
Python 用缩进表示代码块，词法分析器是怎么做到的？它带来什么好处和什么坑（`TabError`）？

## A
大括号语言里，块的边界是 `{` 和 `}` 两个记号。Python 要的效果一样，只是边界来自缩进：词法分析器在每一行开头比较缩进宽度，和栈顶比：变深就产生一个 `INDENT` 记号，变浅就产生一个或多个 `DEDENT` 记号。解析器看到的只是和 `{`/`}` 一样的记号，文法本身不需要知道缩进（这条思路叫**越位规则**，offside rule，来自 ISWIM 与 Haskell 一脉）。

标准库 `tokenize` 能直接看到：
```python
src = "if x:\n    y = 1\nz = 2\n"
# NAME 'if' NAME 'x' OP ':' NEWLINE INDENT NAME 'y' OP '=' NEWLINE DEDENT NAME 'z' ...
```
`INDENT` 出现在 `y = 1` 之前，`DEDENT` 出现在 `z = 2` 之前。

**换来什么**：代码的视觉结构和语法结构永远一致，不可能出现“缩进暗示在 if 里，其实不在”的错觉；没有大括号风格之争；代码更短。

**代价**：
1. 缩进成为语义，复制粘贴、编辑器自动转换空白会改变程序含义；
2. Tab 和空格混用有歧义：同一行文本在不同 Tab 宽度下缩进不同。Python 3 的做法是直接拒绝：
```
    a = 1
\tb = 2
TabError: inconsistent use of tabs and spaces in indentation
```
3. 多行表达式必须靠括号（括号内的换行不产生记号），或行尾反斜杠。

设计者的价值取向很明确：**可读性优先于书写自由度**，并用语法强制所有人写出同一种形状。
