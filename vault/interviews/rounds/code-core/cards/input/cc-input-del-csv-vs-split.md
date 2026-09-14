---
id: cc-input-del-csv-vs-split
node: input.delimited
type: qa
---
## Q
A CSV row is `"Ed, Inc",Ed,ED INC PAYMENTS,ED INC,https://ed.com,"Books, toys"`. What does `line.split(",")` give you, and what do you use instead?

## A
**Eight fields instead of six** — `split` does not know about quotes, so both quoted commas become field separators and every column after the first is shifted.

```python
import csv
for row in csv.reader(sys.stdin):   # or csv.reader(lines)
    ...
```

`csv` also decodes the doubled-quote escape (`"Ed ""The Boss"" Inc"`) and handles a quoted field containing a newline. Use `split` only when the statement guarantees the delimiter never appears inside a value; the moment a field is free text or a human-typed name, reach for `csv`.

## Q zh
一行 CSV 是 `"Ed, Inc",Ed,ED INC PAYMENTS,ED INC,https://ed.com,"Books, toys"`。`line.split(",")` 会给你什么？该用什么代替？

## A zh
**八个字段而不是六个** —— `split` 不认识引号，两个被引号包住的逗号都被当成分隔符，第一列之后的每一列都错位。

```python
import csv
for row in csv.reader(sys.stdin):   # or csv.reader(lines)
    ...
```

`csv` 还会解码双引号转义（`"Ed ""The Boss"" Inc"`），并能处理引号内含换行的字段。只有当题面保证分隔符绝不出现在值里时才用 `split`；一旦某个字段是自由文本或人手输入的名字，就该用 `csv`。
