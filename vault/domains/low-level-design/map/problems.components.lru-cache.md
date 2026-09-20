%% trellis:begin %%
# LRU / LFU 缓存
*设计题（Design Problems） / 基础组件*

O(1) 的 get/put：哈希表加双向链表，LFU 变体，线程安全版本。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/python.data-model|数据模型与特殊方法（Data Model）]], [[domains/low-level-design/map/structure.api|进程内 API 设计]]

## Readings
- [[solution-lru-cache|设计题解：LRU / LFU 缓存（LRU / LFU Cache）]]
- [[src-abhaypaswan-lru-cache|lld-python — lru-cache]]
- [[src-ashishps1-lru-cache|awesome-low-level-design — lru-cache]]
- [[src-donnemartin-lru-cache|system-design-primer — object_oriented_design/lru_cache]]

## Drills
- [[design-lru-cache|Drill：LRU / LFU 缓存]]

## Cards (8)
1. [[problems-lru-cache-store-vs-order-split]]
2. [[problems-lru-cache-sentinel-dll-on1]]
3. [[problems-lru-cache-strategy-pattern-python-form]]
4. [[problems-lru-cache-policy-protocol-choice]]
5. [[problems-lru-cache-overwrite-not-insert]]
6. [[problems-lru-cache-lfu-min-freq-pointer]]
7. [[problems-lru-cache-get-is-write]]
8. [[problems-lru-cache-ttl-wrapper-extension]]
%% trellis:end %%

## Notes
