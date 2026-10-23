---
id: hl-javaq-f-q30-say60
node: java-questions.f-concurrency
type: qa
step: 35
---
## Q
用英文 60 秒回答：How does `ConcurrentHashMap` achieve thread safety? How is it different from `Collections.synchronizedMap`? Why no null keys/values?

## A
结构：Java 8 设计（空桶 CAS、非空桶锁头节点、读无锁）→ 单个方法原子但组合不原子 → 实测 HashMap 丢约 37 万次更新 → 禁 null 的原因 → synchronizedMap 是整表一把锁。

> "Since Java 8 `ConcurrentHashMap` uses CAS to insert into an empty bucket and synchronises only on the head node of a non-empty bucket, so concurrent writers to different buckets don't block each other, and reads are lock-free via volatile reads. The old segment design is gone. Individual operations like `merge` and `putIfAbsent` are atomic, but compositions of separate calls aren't. In a test with eight threads incrementing 16 keys, `HashMap` lost about 370,000 of 1.6 million updates and CHM lost none. It rejects nulls so that `get` returning null unambiguously means absent. `synchronizedMap` by contrast locks the whole map on every call."
