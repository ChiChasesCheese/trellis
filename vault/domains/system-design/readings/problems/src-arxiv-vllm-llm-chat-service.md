---
nodes: [problems.realtime.llm-chat-service]
url: https://arxiv.org/abs/2309.06180
---
# Efficient Memory Management for Large Language Model Serving with PagedAttention

值得读：vLLM/PagedAttention 的原始论文，提出把 KV 缓存像操作系统虚拟内存一样按固定大小
的 block 分页分配，解决长短不一的会话混部时的内部/外部碎片问题，报告相比
FasterTransformer、Orca 等此前系统 2–4 倍吞吐提升、KV 缓存内存浪费接近零。本题解「深入
探讨」第 2 节直接引用这一机制和数字，并把它放进"会话粘性路由 + 按 KV 占用率选副本"的
更完整路由决策里，这是论文本身不涉及的产品层设计。
