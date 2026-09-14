---
id: cc-chrono-parsing-naive-vs-aware
node: chrono.parsing
type: qa
---
## Q
Half the timestamps end in `Z`, half do not. Sorting them together raises `TypeError: can't compare offset-naive and offset-aware datetimes`. Fix it.

## A
**Never let both kinds into one collection — normalize at parse time.**

```python
dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
```

- `fromisoformat` before Python 3.11 rejects a trailing `Z`, hence the replace.
- Decide once what "no offset" means — UTC or some local zone. It changes results, so state the assumption in a comment.
- `replace(tzinfo=...)` *labels* a naive time; `astimezone(...)` *converts* an aware one. Using the wrong one shifts every value by the offset.
- Cheapest option when no zone ever varies: drop the tzinfo entirely and keep integer epoch seconds ([[cc-chrono-parsing-canonical-form]]).

## Q zh
一半时间戳以 `Z` 结尾，一半没有。放在一起排序时抛 `TypeError: can't compare offset-naive and offset-aware datetimes`。怎么修？

## A zh
**别让两种时间进同一个集合 —— 在解析时就归一化。**

```python
dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
```

- Python 3.11 之前的 `fromisoformat` 不接受结尾的 `Z`，所以要先替换。
- 一次性决定「没有 offset」是什么意思 —— UTC 还是某个本地时区。这会改变结果，所以在注释里写明假设。
- `replace(tzinfo=...)` 是给 naive 时间**贴标签**；`astimezone(...)` 是**换算** aware 时间。用错会让每个值整体平移一个 offset。
- 如果时区从不变化，最省事的做法是干脆丢掉 tzinfo，只保留整数 epoch 秒（[[cc-chrono-parsing-canonical-form]]）。
