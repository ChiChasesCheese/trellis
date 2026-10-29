%% trellis:begin %%
# 数据库与搜索引擎

B+ 树、LSM 树、布隆过滤器、WAL 与 MVCC、连接算法与外部排序、缓冲池替换、倒排索引。

## Topics
- [[domains/under-the-hood/map/storage.btree|B+ 树：InnoDB 与 SQLite]]
- [[domains/under-the-hood/map/storage.lsm|LSM 树：RocksDB / LevelDB]]
- [[domains/under-the-hood/map/storage.bloom|布隆过滤器：LSM 的读路径]]
- [[domains/under-the-hood/map/storage.wal-mvcc|WAL 与 MVCC]]
- [[domains/under-the-hood/map/storage.query-exec|查询执行：哈希连接、排序归并、外部排序]]
- [[domains/under-the-hood/map/storage.buffer-pool|缓冲池替换：中点 LRU 与时钟扫描]]
- [[domains/under-the-hood/map/storage.inverted-index|Lucene / Elasticsearch 的倒排索引]]
%% trellis:end %%

## Notes
