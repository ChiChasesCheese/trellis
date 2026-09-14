---
id: cc-input-norm-whitespace-collapse
node: input.normalization
type: qa
---
## Q
`"General   Merchandise"` with a doubled space must match the blacklist entry `"GENERAL MERCHANDISE"`, and a field of two spaces must count as empty. One idiom does both — what is it?

## A
**`" ".join(s.split())`** — the no-argument `split()` splits on runs of any whitespace and discards leading and trailing runs, so tabs, doubled spaces and a stray newline all collapse in one call, and `"  "` becomes `""`.

```python
key = " ".join(s.split()).casefold()
if not key:            # whitespace-only field is empty
    ...
```

`s.strip()` alone leaves interior runs; `s.replace("  ", " ")` misses triples and tabs. Do it once at the boundary, and treat "empty after normalization" as a distinct, decided case.

## Q zh
带双空格的 `"General   Merchandise"` 必须匹配黑名单条目 `"GENERAL MERCHANDISE"`，而只有两个空格的字段必须算作空。一个写法两件事都做到 —— 是哪个？

## A zh
**`" ".join(s.split())`** —— 不带参数的 `split()` 按任意空白的连续段切分并丢弃首尾空白，于是制表符、双空格、误入的换行都在一次调用里折叠掉，`"  "` 也变成 `""`。

```python
key = " ".join(s.split()).casefold()
if not key:            # whitespace-only field is empty
    ...
```

只用 `s.strip()` 会留下中间的连续空白；`s.replace("  ", " ")` 漏掉三连空格和制表符。在边界处做一次，并把"归一化后为空"当作一个独立且已作决定的情形。
