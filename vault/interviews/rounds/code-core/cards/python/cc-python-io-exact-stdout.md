---
id: cc-python-io-exact-stdout
node: python.io
type: qa
---
## Q
`print` per line, or `sys.stdout.write("\n".join(out))`? Choose for 10^5 output lines, and state the trailing-newline rule.

## A
**Build a list, join once, write once.**

```python
stdout.write("\n".join(out) + ("\n" if out else ""))
```

- `print` per line performs a separate write and appends `\n` each time; the join is several times faster at 10^5 lines.
- The `if out` guard is the point: on empty output you must emit **nothing**, not a lone newline. Comparators commonly strip one trailing newline but not a leading blank line.
- Never `print` a Python container — `str(list)` and `str(dict)` are not an output format, and a debug `print(rows)` left in place produces exactly that.
- Render in one place, at write time, so a format change is a one-line change.

## Q zh
逐行 `print`，还是 `sys.stdout.write("\n".join(out))`？在 10^5 行输出的场景下选一个，并说出结尾换行的规则。

## A zh
**攒成 list，join 一次，write 一次。**

```python
stdout.write("\n".join(out) + ("\n" if out else ""))
```

- 逐行 `print` 每次都要单独写一次并追加 `\n`；在 10^5 行上 join 要快好几倍。
- `if out` 这个守卫才是重点：输出为空时你必须**什么都不打印**，而不是打一个孤零零的换行。比对器通常会去掉一个结尾换行，但不会去掉开头的空行。
- 绝不要 `print` 一个 Python 容器 —— `str(list)` 和 `str(dict)` 不是输出格式，而残留的调试 `print(rows)` 产生的正是它。
- 只在一个地方、在写出时渲染，这样改格式就是改一行。
