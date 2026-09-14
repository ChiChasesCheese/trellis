---
id: cc-input-struct-repeated-keys
node: input.structured
type: qa
---
## Q
The same key appears twice in one record: `amount=5&amount=7`. What are the two reasonable policies, and how does the choice show up in code?

## A
**Last value wins, or collect every value into a list.** The statement usually says ("duplicate key → last value wins"); when it does not, last-wins is the safer default because it matches how a dict assignment already behaves.

```python
d[k] = v                       # last wins — the default of the loop
d.setdefault(k, []).append(v)  # collect
```

The trap is choosing accidentally: `parse_qs` collects (and you then compare a list against a string), while a hand-written loop last-wins. Also decide what a *repeated setup line* means — a repeated threshold usually overwrites, a repeated fraud-code line usually unions.

## Q zh
同一条记录里某个 key 出现两次：`amount=5&amount=7`。两种合理策略是什么？这个选择在代码里如何体现？

## A zh
**后者覆盖，或者把每个值收集成列表。** 题面通常会说明（「重复 key → 后者生效」）；没说时，后者覆盖是更安全的默认，因为它与 dict 赋值的天然行为一致。

```python
d[k] = v                       # last wins — the default of the loop
d.setdefault(k, []).append(v)  # collect
```

坑在于**无意中**做了选择：`parse_qs` 是收集（于是你会拿列表去和字符串比较），而手写循环是后者覆盖。另外还要决定**重复的配置行**意味着什么 —— 重复的阈值通常是覆盖，重复的 fraud-code 行通常是取并集。
