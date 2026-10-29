%% trellis:begin %%
# client-go 的 Indexer：主存储 + 二级索引
*数据结构组合：开源框架里的类设计*

本地缓存除了按 key 查，还要按命名空间、按标签查：一张主表加若干张“索引名 → 索引值 → key 集合”的二级索引，每次增删改都要同步更新所有索引。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-k8s-indexer-1-need]]
2. [[uth-compose-k8s-indexer-2-parts]]
3. [[uth-compose-k8s-indexer-3-code]]
4. [[uth-compose-k8s-indexer-4-real]]
5. [[uth-compose-k8s-indexer-5-interview]]
%% trellis:end %%

## Notes
