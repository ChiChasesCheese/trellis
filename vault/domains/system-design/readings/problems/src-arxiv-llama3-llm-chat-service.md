---
nodes: [problems.realtime.llm-chat-service]
url: https://arxiv.org/abs/2407.21783
---
# The Llama 3 Herd of Models

值得读：官方架构表给出 70B 变体的具体形状——80 层、8,192 隐藏维度、64 个注意力头、
8 个 KV 头（分组查询注意力/GQA）、128K 上下文窗口。本题解用这套公开数字作为容量估算里
KV 缓存字节数计算的模型形状假设（而不是编造一个不存在的公司真实模型形状），论文本身
是训练与评测报告，不涉及服务层设计，这是本题解唯一借用它的地方。

%% trellis:begin %%
## Source
[Open the original ↗](https://arxiv.org/abs/2407.21783)
%% trellis:end %%
