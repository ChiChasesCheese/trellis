---
nodes: [problems.realtime.llm-chat-service]
url: https://arxiv.org/abs/2401.09670
---
# DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

值得读：论证 prefill（计算受限，决定 TTFT）和 decode（显存带宽受限，决定逐 token 延迟）
应该跑在物理分离的 GPU 池上，而不是混部在同一批请求里；报告相比同 SLO 下的混部系统最高
7.4 倍吞吐，或同吞吐下 12.6 倍更紧的延迟 SLO。本题解「深入探讨」第 3 节引用这一方案和
数字，并补充了对话场景下 prompt 长度方差（几个 token 到几千 token）比论文评测负载更
极端，因此这个取舍在聊天产品里价值更明显这一论点。

%% trellis:begin %%
## Source
[Open the original ↗](https://arxiv.org/abs/2401.09670)

## Archived copy
![[src-arxiv-distserve-llm-chat-service-clip]]
%% trellis:end %%
