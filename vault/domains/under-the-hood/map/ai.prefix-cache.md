%% trellis:begin %%
# 前缀缓存：基数树与按块哈希
*AI 工程里的数据结构与算法*

很多请求共享同一段系统提示词：SGLang 的 RadixAttention 把缓存过的 token 序列存进基数树，按 LRU 淘汰叶子；vLLM 的自动前缀缓存给每个满块算一个连同前缀的哈希，用哈希表查找。

## Cards (3)
1. [[uth-ai-prefix-cache-1-radix-tree]]
2. [[uth-ai-prefix-cache-2-block-hash]]
3. [[uth-ai-prefix-cache-3-eviction]]
%% trellis:end %%

## Notes
