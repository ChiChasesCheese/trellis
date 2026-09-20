---
nodes: [problems.realtime.llm-chat-service]
url: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
---
# Prompt caching (Anthropic API documentation)

值得读：Anthropic 官方文档描述的前缀缓存实现——显式 `cache_control` 断点、按最近 20 个
断点向前查找匹配、缓存写入按 TTL（5 分钟/1 小时）比正常输入贵 1.25–2 倍，缓存命中读取
比正常输入便宜约 90%。本题解「深入探讨」第 3 节引用这些机制细节，并与 OpenAI 的自动
前缀缓存对比说明"省去重复 prefill 计算"这件事有不止一种工程实现；文档本身只讲计费和
API 行为，不涉及 prefill/decode 物理分离，这是本题解在其上叠加的一层。

%% trellis:begin %%
## Source
[Open the original ↗](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching)

## Archived copy
![[src-anthropic-llm-chat-service-clip]]
%% trellis:end %%
