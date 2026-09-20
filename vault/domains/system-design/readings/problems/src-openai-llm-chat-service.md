---
nodes: [problems.realtime.llm-chat-service]
url: https://developers.openai.com/api/docs/guides/prompt-caching
---
# Prompt caching (OpenAI API documentation)

值得读：OpenAI 官方文档描述的前缀缓存实现——对 1,024 token 以上的前缀自动生效、无需
显式断点，缓存命中的部分按折扣价计费，缓存生命周期在几分钟到一小时量级。与 Anthropic
的显式断点式实现形成对照，本题解「深入探讨」第 3 节用两者共同说明前缀缓存这一机制的
普适性，而不是某一家的专属实现；本题解据此设计的会话粘性路由（尽量让同一对话的后续
轮次命中同一副本的前缀缓存）是文档本身不涉及的服务端路由决策。

%% trellis:begin %%
## Source
[Open the original ↗](https://developers.openai.com/api/docs/guides/prompt-caching)

## Archived copy
![[src-openai-llm-chat-service-clip]]
%% trellis:end %%
