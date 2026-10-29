%% trellis:begin %%
# Go 的 sync.Map：只读表 + 脏表，以及 1.24 起的并发哈希字典树
*数据结构组合：开源框架里的类设计*

读多写少时怎样让读完全不加锁：旧实现（1.25 及以前的默认）用一张原子读取的只读表、一张加锁的脏表，读不到时去脏表找并累计未命中，次数够了就把脏表整体提升为只读表；Go 1.24 起默认改成并发哈希字典树（HashTrieMap）。

**Core** — part of the first pass through this subject.

## Cards (4)
1. [[uth-compose-go-sync-map-1-need]]
2. [[uth-compose-go-sync-map-2-parts]]
3. [[uth-compose-go-sync-map-3-code]]
4. [[uth-compose-go-sync-map-4-real]]
%% trellis:end %%

## Notes
