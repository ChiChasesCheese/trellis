%% trellis:begin %%
# AI 工程里的数据结构与算法

大模型训练与推理系统里天天用到的结构：分词、采样、KV 缓存分页、前缀缓存、向量检索、数据去重、自动求导。

## Topics
- [[domains/under-the-hood/map/ai.tokenizer|分词器：BPE 的贪心合并与 Unigram 的动态规划]]
- [[domains/under-the-hood/map/ai.sampling|采样：top-k 与 top-p]]
- [[domains/under-the-hood/map/ai.paged-kv|vLLM 的 PagedAttention：KV 缓存分页]]
- [[domains/under-the-hood/map/ai.prefix-cache|前缀缓存：基数树与按块哈希]]
- [[domains/under-the-hood/map/ai.vector-search|向量检索：HNSW 与 IVF]]
- [[domains/under-the-hood/map/ai.dedup|训练数据去重：MinHash、LSH 与并查集]]
- [[domains/under-the-hood/map/ai.autograd|自动求导：计算图上的拓扑排序]]
%% trellis:end %%

## Notes
