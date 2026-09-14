---
id: cc-round-debug-diff-the-bytes
node: round.debugging
type: qa
---
## Q
Your output *looks* identical to the expected output but the test still fails. How do you find the difference?

## A
**Compare representations, not renderings.** A trailing space, `\r\n`, a missing final newline, a non-breaking space and a tab all render as "the same" in a terminal.

```python
for i, (g, w) in enumerate(zip(got.splitlines(), want.splitlines())):
    if g != w:
        print(i, repr(g), repr(w), file=sys.stderr); break
print(len(got.splitlines()), len(want.splitlines()), file=sys.stderr)
```

`repr()` shows the whitespace; the line-count print catches the case where one side has an extra blank or missing last line — the most common byte-level failure of all.

## Q zh
你的输出**看起来**和期望输出一模一样，测试却还是失败。怎么找出差异？

## A zh
**比较表示，而不是比较渲染结果。** 行尾空格、`\r\n`、缺失的末尾换行、不换行空格和制表符，在终端里看起来"都一样"。

```python
for i, (g, w) in enumerate(zip(got.splitlines(), want.splitlines())):
    if g != w:
        print(i, repr(g), repr(w), file=sys.stderr); break
print(len(got.splitlines()), len(want.splitlines()), file=sys.stderr)
```

`repr()` 会把空白显示出来；打印行数则能抓到一侧多了空行或少了末行的情况 —— 这是最常见的字节级失败。
