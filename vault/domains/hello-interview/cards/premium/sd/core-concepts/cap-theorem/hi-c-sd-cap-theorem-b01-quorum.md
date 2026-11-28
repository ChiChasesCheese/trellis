---
id: hi-c-sd-cap-theorem-b01-quorum
node: sd.core-concepts.cap-theorem.beyond
type: qa
step: 1
---
## Q
**CAP 定理 · 法定人数读写：R + W > N**｜拓展 · 加分
Dynamo 风格数据库（Cassandra、DynamoDB 一类）怎么用副本数 N、写确认数 W、读确认数 R 调节一致性？

## A
**模式。** 法定人数（quorum）重叠。
```python
from itertools import combinations

N, W, R = 3, 2, 2
replicas = ["r1", "r2", "r3"]

# 任意 W 个副本构成的写集合，与任意 R 个副本构成的读集合，一定相交
for ws in combinations(replicas, W):
    for rs in combinations(replicas, R):
        assert set(ws) & set(rs), (ws, rs)

# 反例：N=3, W=1, R=1，读可能完全碰不到最新写
N, W, R = 3, 1, 1
bad = [(ws, rs) for ws in combinations(replicas, W)
       for rs in combinations(replicas, R) if not set(ws) & set(rs)]
print(len(bad))      # 6 种组合读不到最新写
```
- **规则：** 当 R + W > N，任何读集合都至少包含一个拿到最新写的副本，读到最新值（配合版本号选最新的一份）。
- **调节：** N=3、W=2、R=2 兼顾；W=1 则写快但读要 R=3 才保证；R=1 则读快但写要 W=3。W 越大，写可用性越低。
- **注意：** 这只是"通常"强一致，宽松法定人数（sloppy quorum，故障时借用其他节点）、并发写、时钟问题都可能让它不是严格的线性一致，不要说成保证。
- **关系到 CAP：** 小的 W 与 R 偏向可用性和延迟；大的 W 与 R 偏向一致性，故障节点多了就拿不够确认，等于牺牲可用性。
