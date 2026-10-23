---
id: hl-cq-q18-million-key-numbers
node: cpp-questions.d-containers
type: qa
step: 9
---
## Q
100 万个随机 key，`std::map`、`unordered_map`、排序 `vector` 的建表和查询各约多少毫秒？

## A
`-O2`、Apple Silicon，只看量级：

| 1M 个 key | `std::map` | `unordered_map` | 排序 vector |
|---|---|---|---|
| 建表 | 159 ms | 26 ms | 45 ms |
| 查询 | 146 ms | 13 ms | 45 ms |

结论：哈希表查询比树快约 10 倍；排序 `vector` + 二分居中，且没有逐节点分配。
