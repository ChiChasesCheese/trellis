---
id: hl-cache-hashmap-get-cost
node: foundations.cpu-cache-locality
type: qa
step: 44
---
## Q
为什么 `HashMap.get` 是 O(1)，却比顺序读数组慢那么多？

## A
`HashMap.get` 要：算哈希、读桶数组（随机位置，缓存缺失）、读 `Node`（又一次缺失）、比较 key（可能读 key 对象，第三次缺失）。

O(1) 只说明操作数与 n 无关，不说明每步都在缓存里。`get` 约 10 ns（缓存友好的 100 万 key 场景），顺序读数组 < 1 ns。
