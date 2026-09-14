---
id: distributed-crdt-counters
node: distributed.crdt
type: cloze
---
A G-counter (grow-only) keeps {{c1::one slot per replica; each replica increments only its own slot}}; the value is {{c2::the sum of all slots}}, and merge is {{c3::element-wise max}} — max is idempotent, so re-merging never double-counts, which is exactly why a single shared integer can't work (summing two copies double-counts, max loses increments). A PN-counter supports decrement by {{c4::pairing two G-counters — increments and decrements — and reporting P − N}}. Limitation worth stating: it can transiently go below an intended floor (e.g. negative inventory), because no CRDT can enforce a global invariant without coordination.

## zh
G-Counter（只增）维护{{c1::每个副本一个槽；每个副本只递增自己的槽}}；值是{{c2::所有槽的和}}，合并是{{c3::逐元素最大值}}——最大值是幂等的，所以重新合并永远不会双计，这正是单个共享整数无法工作的原因（求和两份拷贝会双计，最大值会丢失递增）。PN-Counter 通过{{c4::配对两个 G-Counter——递增和递减——报告 P − N}}来支持递减。限制值得说明：它可能暂时跌入预期下界（如负库存），因为没有 CRDT 可以在没有协调的情况下强制全局不变量。
