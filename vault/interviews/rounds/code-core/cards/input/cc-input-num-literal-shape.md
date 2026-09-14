---
id: cc-input-num-literal-shape
node: input.numbers
type: qa
---
## Q
A configuration line is `THRESHOLD,<mcc>,<value>` where `3` means "three fraudulent charges" and `0.25` means "a quarter of all charges" — and `1.0` means a ratio while `1` means a count. How do you parse it?

## A
**Dispatch on the shape of the literal, before converting it.**

```python
if "." in tok:
    kind, num, den = "ratio", int(tok.replace(".", "")), 10 ** len(tok.split(".")[1])
else:
    kind, num, den = "count", int(tok), 1
```

`float(tok)` destroys the distinction — `1.0` and `1` both become `1.0` — and it also destroys exactness, which the later comparison needs. The general rule: when the *spelling* of a literal carries meaning, branch on the string and convert inside the branch. See [[cc-rules-ratio-decimal-literal-as-fraction]].

## Q zh
一行配置是 `THRESHOLD,<mcc>,<value>`，其中 `3` 表示"三笔欺诈扣款"，`0.25` 表示"全部扣款的四分之一" —— 并且 `1.0` 是比率而 `1` 是计数。怎么解析？

## A zh
**在转换之前，先按字面量的形状分派。**

```python
if "." in tok:
    kind, num, den = "ratio", int(tok.replace(".", "")), 10 ** len(tok.split(".")[1])
else:
    kind, num, den = "count", int(tok), 1
```

`float(tok)` 会毁掉这个区分 —— `1.0` 和 `1` 都变成 `1.0` —— 同时也毁掉后续比较所需的精确性。通则是：当字面量的**写法**携带含义时，就对字符串分支，并在分支内部做转换。见 [[cc-rules-ratio-decimal-literal-as-fraction]]。
