---
id: cc-input-del-header-driven
node: input.delimited
type: qa
---
## Q
The CSV has a header row, the columns may arrive in any order, and extra columns may be present. How do you read a field?

## A
**By name, through `csv.DictReader`, with the header names stripped once.**

```python
reader = csv.DictReader(lines)
reader.fieldnames = [h.strip() for h in reader.fieldnames]
for row in reader:
    amount = int(row["amount"].strip())
```

Positional indexing breaks the moment the grader shuffles the columns — a documented test in header-driven problems. Two further details: a header cell can carry a UTF-8 BOM (open with `encoding="utf-8-sig"` or strip it), and a *missing* named column should be one explicit check with a decided policy, not a `KeyError` in the middle of the loop.

## Q zh
CSV 带表头，列的顺序任意，还可能有多余的列。怎么读某个字段？

## A zh
**按名字读，用 `csv.DictReader`，表头名先统一 strip 一次。**

```python
reader = csv.DictReader(lines)
reader.fieldnames = [h.strip() for h in reader.fieldnames]
for row in reader:
    amount = int(row["amount"].strip())
```

一旦评测机打乱列序，按下标取值就崩 —— 这在 header 驱动的题里是有明确测试的。还有两个细节：表头单元格可能带 UTF-8 BOM（用 `encoding="utf-8-sig"` 打开或手工去掉）；**缺失**的列应当是一处明确的检查加一条既定策略，而不是循环中途抛出的 `KeyError`。
