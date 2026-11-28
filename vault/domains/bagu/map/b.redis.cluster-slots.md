%% trellis:begin %%
# Redis Cluster 的哈希槽与重定向（Hash Slot, MOVED/ASK）
*B 其余知识点 / Redis*

Cluster 用 16384 个哈希槽分片，客户端靠 MOVED/ASK 重定向，多 key 操作要求同槽。

## Cards (1)
1. [[bagu-cluster-slots-1-hash-slot-redirect]]
%% trellis:end %%

## Notes
