---
id: pay-reconciliation-matching-code
node: reconciliation.matching
type: qa
step: 5
---
## Q
请写出把内部记录与渠道记录按键做精确匹配、并把每一行归为"一致 / 长款 / 短款 / 金额不一致 / 状态不一致"的最小实现，并说明它的输出怎么读。

## A
```python
Row = tuple[int, str]  # (amount in minor units, status)

def reconcile(ours: dict[str, Row], theirs: dict[str, Row]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {k: [] for k in ("ok", "long", "short", "amount", "status")}
    for key in sorted(ours.keys() | theirs.keys()):
        a, b = ours.get(key), theirs.get(key)
        kind = ("short" if b is None else "long" if a is None
                else "amount" if a[0] != b[0] else "status" if a[1] != b[1] else "ok")
        out[kind].append(key)
    return out
```
用 o1 到 o5 五笔跑，实际输出：
```
{'ok': ['o1'], 'long': ['o4'], 'short': ['o3'], 'amount': ['o2'], 'status': ['o5']}
```
读法：
- o1 双方一致。
- o2 双方金额不同（2500 对 2400），渠道少 100，查是否有部分退款或手续费混入。
- o3 我方有、渠道无，是短款，优先级最高。
- o4 渠道有、我方无，是长款，补记或退款。
- o5 我方处理中、渠道已成功，状态不一致，用渠道状态推进。

要点：键集合取并集，一次遍历同时得到两个方向的缺失，复杂度 O(n)；金额用整数，避免浮点比较；先做存在性判断，再做金额，最后做状态，顺序决定了一行只会落入一类。
