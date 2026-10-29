%% trellis:begin %%
# vLLM 的 PagedAttention：KV 缓存分页
*AI 工程里的数据结构与算法*

推理时每个请求的 KV 缓存越长越大，连续分配会浪费和碎片化；vLLM 把它切成固定大小的块，用块表映射逻辑块到物理块，空闲块放进空闲列表，共享前缀用引用计数和写时复制：就是操作系统的分页。

## Cards (3)
1. [[uth-ai-paged-kv-1-blocks]]
2. [[uth-ai-paged-kv-2-free-list]]
3. [[uth-ai-paged-kv-3-cow]]
%% trellis:end %%

## Notes
