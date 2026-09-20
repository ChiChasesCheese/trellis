%% trellis:begin %%
# 内存键值存储（In-Memory Key-Value Store）
*设计题（Design Problems） / 基础组件*

分关递进的机考题型：基本读写 → 扫描与前缀 → TTL → 事务或备份恢复。

**Requires:** [[domains/low-level-design/map/structure.storage|内存持久化（In-Memory Persistence）]]

## Readings
- [[solution-kv-store|设计题解：内存键值存储（In-Memory Key-Value Store）]]
- [[src-codezym-kv-store|CodeZym — Amazon machine coding questions]]
- [[src-workattech-kv-store|workat.tech — Design a Key-Value Store]]

## Drills
- [[design-kv-store|Drill：内存键值存储（In-Memory Key-Value Store）]]

## Cards (8)
1. [[problems-kv-store-two-independent-ttl-lines]]
2. [[problems-kv-store-apply-field-symmetric]]
3. [[problems-kv-store-expiry-recomputed-not-cached]]
4. [[problems-kv-store-undo-log-vs-copy-on-write]]
5. [[problems-kv-store-commit-folds-into-parent]]
6. [[problems-kv-store-undo-log-is-command-pattern]]
7. [[problems-kv-store-single-lock-for-transactions]]
8. [[problems-kv-store-begin-deep-copy-mistake]]
%% trellis:end %%

## Notes
