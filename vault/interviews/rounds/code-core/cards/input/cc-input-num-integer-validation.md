---
id: cc-input-num-integer-validation
node: input.numbers
type: qa
---
## Q
A field must be "an integer ≥ 0". Which of `25.00`, `abc`, `-1`, `` , `0100`, `+5`, ` 7 ` are valid, and how do you test it?

## A
**Valid: `0100` (→ 100), `+5`, ` 7 ` — `int()` accepts a sign and surrounding whitespace. Invalid: `25.00`, `abc`, the empty string, and `-1` (parses, but fails the range check).**

```python
def as_nonneg_int(tok):
    try:
        v = int(tok)
    except ValueError:
        return None
    return v if v >= 0 else None
```

Two separate checks: *is it an integer* and *is it in range*. Collapsing them into one regex loses the range message, and `str.isdigit()` is not the test — it rejects `+5` and ` 7 ` and accepts non-ASCII digits.

## Q zh
某字段必须是"≥ 0 的整数"。`25.00`、`abc`、`-1`、空串、`0100`、`+5`、` 7 ` 中哪些合法？怎么判？

## A zh
**合法：`0100`（→ 100）、`+5`、` 7 ` —— `int()` 接受符号和两侧空白。不合法：`25.00`、`abc`、空串，以及 `-1`（能解析，但过不了范围检查）。**

```python
def as_nonneg_int(tok):
    try:
        v = int(tok)
    except ValueError:
        return None
    return v if v >= 0 else None
```

这是两个独立检查：**是不是整数**和**在不在范围内**。把它们压进一个正则会丢掉范围这层信息；而 `str.isdigit()` 不是正确判据 —— 它拒绝 `+5` 和 ` 7 `，却接受非 ASCII 数字。
