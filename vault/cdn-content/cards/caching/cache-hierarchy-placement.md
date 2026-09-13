---
id: cache-hierarchy-placement
node: caching.hierarchy
type: qa
---
## Q
How should object popularity and size influence placement across memory, edge disk, shield, and object storage?

## A
Keep small hot objects in scarce low-latency memory; use larger edge/shield tiers for the warm working set; leave cold long-tail objects in durable object storage. Optimize expected latency, origin load and cost per byte, not raw object count. Admission and maximum-object-size rules prevent one huge or one-hit object from evicting many useful entries.

## Q zh
object popularity 与 size 应如何影响它在 memory、edge disk、shield、object storage 之间的 placement？

## A zh
把小而热的 object 放在稀缺的低延迟 memory；较大的 edge/shield tier 保存 warm working set；cold long-tail object 留在 durable object storage。优化 expected latency、origin load 与 cost per byte，而不是 raw object count。admission 与 maximum-object-size rule 可防止一个巨大或只访问一次的 object 驱逐大量有用 entry。
