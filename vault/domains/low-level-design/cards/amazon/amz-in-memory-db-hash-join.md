---
id: amz-in-memory-db-hash-join
node: amazon.amz-in-memory-db
type: qa
step: 4
tags: [grown]
---
## Q
在内存数据库里，两张表按键连接，哈希连接怎么做、复杂度多少？举一个输入和输出。

## A
先扫右表，把键非 NULL 的行放进 `键 → 行列表` 的字典（构建，O(|R|)）；再扫左表，用键取匹配行（探测，O(|L| + 输出行数)）。嵌套循环是 O(|L|·|R|)。

```python
buckets = defaultdict(list)
for r in right_rows:
    if r[rk] is not None:
        buckets[r[rk]].append(r)
for l in left_rows:
    hits = buckets.get(l[lk], []) if l[lk] is not None else []
    out += [{**l, **h} for h in hits]
    if not hits and kind == "left":
        out.append({**l, **null_right})
```
ann、bob、cat 连订单（ann 两单、bob 一单）：内连接 3 行，左连接 4 行，多出 cat 配 NULL。
