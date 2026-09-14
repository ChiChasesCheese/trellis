---
id: cc-python-io-part-dispatch
node: python.io
type: qa
---
## Q
A multi-part problem sends `PART 3` as an optional first line, then the data. Structure `main` so each part stays independently testable.

## A
```python
def main(stdin=sys.stdin, stdout=sys.stdout):
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part, rows = LAST, lines
    if lines and lines[0].startswith("PART"):
        part, rows = int(lines[0].split()[1]), lines[1:]
    out = HANDLERS.get(part, HANDLERS[LAST])(rows)
    stdout.write("\n".join(out) + ("\n" if out else ""))
```

- Every `partN(rows) -> list[str]` is a **pure function of plain data** — no I/O inside — so a test calls it directly with a list of strings and compares a list of strings.
- Default to the **last** part when the header is missing: a grader often runs the finished program with no `PART` line.
- Later parts may call earlier ones; the dispatch stays a one-line table ([[cc-python-io-main-seam]]).

## Q zh
一道多 part 的题把 `PART 3` 作为可选的第一行发过来，之后是数据。把 `main` 组织成让每个 part 都能独立测试的样子。

## A zh
```python
def main(stdin=sys.stdin, stdout=sys.stdout):
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part, rows = LAST, lines
    if lines and lines[0].startswith("PART"):
        part, rows = int(lines[0].split()[1]), lines[1:]
    out = HANDLERS.get(part, HANDLERS[LAST])(rows)
    stdout.write("\n".join(out) + ("\n" if out else ""))
```

- 每个 `partN(rows) -> list[str]` 都是**普通数据的纯函数** —— 内部没有 I/O —— 于是测试可以直接传一个字符串列表进去、再比对一个字符串列表。
- 表头缺失时默认走**最后**一个 part：评测机常常不带 `PART` 行直接跑完成品。
- 后面的 part 可以调用前面的；分派本身保持为一行表（[[cc-python-io-main-seam]]）。
