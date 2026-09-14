---
id: cc-input-del-variable-length-rows
node: input.delimited
type: qa
---
## Q
One statement says "missing trailing columns count as empty, extra columns are ignored"; another says "a row that does not have exactly six fields is corrupted". How do you write the parser so both are one line apart?

## A
**Check the length explicitly and branch on the stated policy; never let tuple unpacking make the decision.**

```python
if len(fields) != EXPECTED:          # strict form
    skipped += 1; continue
fields = (fields + [""] * EXPECTED)[:EXPECTED]   # lenient form
```

`a, b, c = fields` raises on both too few and too many, which conflates two cases the specs treat differently, and it crashes instead of counting. Read the statement for which policy applies and write the check where a reader can see it — the count of skipped rows is often itself part of the output.

## Q zh
一份题面说「缺失的末尾列按空处理，多余的列忽略」；另一份说「字段数不恰好是 6 的行是损坏行」。怎么写解析器，让两者只差一行？

## A zh
**显式检查长度并按题面策略分支；绝不让元组解包替你做决定。**

```python
if len(fields) != EXPECTED:          # strict form
    skipped += 1; continue
fields = (fields + [""] * EXPECTED)[:EXPECTED]   # lenient form
```

`a, b, c = fields` 在字段过少和过多时都会抛异常，把两种题面区别对待的情形混为一谈，而且是崩溃而不是计数。读清题面适用哪条策略，并把检查写在读者看得见的位置 —— 被跳过的行数本身常常就是输出的一部分。
