---
id: problems-llm-chat-service-prefill-decode-disaggregation-tradeoff
node: problems.realtime.llm-chat-service
type: qa
step: 4
tags: [grown]
---
## Q
In a chat service that colocates prefill and decode on the same batch of GPUs, why does one user pasting a long document into the chat degrade the token-streaming latency other users are currently experiencing, and what's the alternative architecture?

## A
Prefill (processing an entire prompt in one parallel pass) is compute-bound, while decode (producing one token at a time) is memory-bandwidth-bound — the two phases have opposite resource profiles. When they run on the same batch of GPUs, a large prefill job for one long document consumes compute that the GPU would otherwise use to advance the next decode step for every other in-flight conversation, so those other users see their token stream visibly stall while the big prefill runs. The alternative — prefill/decode disaggregation — runs the two phases on physically separate GPU pools, each tuned for its own bottleneck, and hands off the KV cache between pools once prefill finishes; published benchmarks of this approach report throughput gains of several times, or equivalently much tighter latency SLOs, versus keeping both phases colocated on the same GPUs.

## Q zh
在一个把 prefill 和 decode 混部在同一批 GPU 上的聊天服务中，为什么某个用户粘贴一大段长文档会拖慢其他用户当前正在接收的逐字流式输出？替代架构是什么？

## A zh
Prefill（一次并行处理整个 prompt）是计算受限的，而 decode（一次生成一个 token）是显存带宽受限的——两个阶段的资源画像正好相反。当它们跑在同一批 GPU 上时，一个长文档的大 prefill 任务会占用本该被 GPU 用来推进其他所有在飞会话下一个 decode 步骤的计算资源，于是其他用户会明显看到自己的 token 流在这段大 prefill 运行期间卡顿。替代架构——prefill/decode 分离——把两个阶段调度到物理独立的 GPU 池上，各自针对自己的瓶颈优化，prefill 完成后把 KV 缓存移交给 decode 池；已发表的基准测试报告这种方案相比两阶段混部在同一批 GPU 上，能达到数倍的吞吐提升，或者等价地在同吞吐下把延迟 SLO 收紧数倍。
