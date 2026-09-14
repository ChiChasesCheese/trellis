---
id: cc-input-lp-blank-lines-and-spaces
node: input.line-protocols
type: qa
---
## Q
The spec says blank lines are ignored and spaces around commas are tolerated. Where does that live in your program?

## A
**In the reader, once — never repeated inside the handlers.**

```python
for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    fields = [f.strip() for f in line.split(",")]
```

Three traps this closes: a line of only spaces is blank (`raw == "\n"` is not the test — `raw.strip()` is); the file's trailing newline yields one empty final line; and a field left un-stripped turns `" 5"` into a parse error or `"acct_a "` into a second, distinct key. Tolerated whitespace that reaches a dict key is the bug you will not see in the output.

## Q zh
题面说空行忽略、逗号周围的空格可容忍。这条规则放在程序的哪里？

## A zh
**放在读取处，只写一次 —— 绝不在各个 handler 里重复。**

```python
for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    fields = [f.strip() for f in line.split(",")]
```

它一次堵掉三个坑：只有空格的行也是空行（判据不是 `raw == "\n"` 而是 `raw.strip()`）；文件末尾的换行会多出一个空行；没有 strip 的字段会把 `" 5"` 变成解析错误、把 `"acct_a "` 变成另一个不同的 key。混进 dict key 的"可容忍空白"，正是你在输出里看不出来的那个 bug。
