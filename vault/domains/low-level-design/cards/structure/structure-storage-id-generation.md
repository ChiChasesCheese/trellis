---
id: structure-storage-id-generation
node: structure.storage
type: cloze
---
Id generation in an in-memory store: `nextId++` on a plain `long` is a {{c1::lost-update race (read-modify-write is not atomic)}} under concurrency — use {{c2::`AtomicLong.incrementAndGet()`}} for compact, ordered ids. Prefer {{c3::UUIDs}} when ids must be generated **without coordination** (multiple instances, client-side creation), accepting that they're unordered and bulky. Never derive the id from mutable business fields — it must stay stable while everything else changes.


## zh
内存存储中的 ID 生成: 平面 `long` 上的 `nextId++` 是一个 {{c1::丢失更新竞争（读-改-写不是原子的）}}在并发下 — 使用 {{c2::`AtomicLong.incrementAndGet()`}}来获取紧凑的、有序的 id。当 id 必须被生成**不加协调**（多个实例、客户端侧创建）时更喜欢 {{c3::UUID}}，接受他们是无序的和庞大的。永不从可变商业字段推导 id — 它必须保持稳定当一切其他改变时。
