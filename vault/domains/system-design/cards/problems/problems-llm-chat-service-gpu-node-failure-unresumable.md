---
id: problems-llm-chat-service-gpu-node-failure-unresumable
node: problems.realtime.llm-chat-service
type: qa
step: 7
tags: [grown]
---
## Q
In an LLM chat service, a GPU node dying mid-generation is a fundamentally different failure than a client's network connection dropping mid-generation — why can't the reconnect-and-resume mechanism designed for dropped client connections rescue a session whose GPU node has failed?

## A
The reconnect-and-resume mechanism works because generation and its KV cache keep running on a healthy GPU node regardless of the client's connection state, so a client that comes back can simply be handed the buffered output and the still-live stream. When the GPU node itself dies, the KV cache for every session it was holding is lost along with it — replicating KV cache across nodes for every in-flight session would be far more expensive than the failure it protects against, so it isn't done. There is nothing left to resume: the client's SSE stream simply terminates, and the service can only offer a fresh generation attempt, distinguished from a duplicate submission by the client's idempotency key representing a new attempt rather than a retry of a completed one.

## Q zh
在一个 LLM 聊天服务中，GPU 节点在生成中途宕机和客户端网络连接在生成中途断开，是两种本质不同的故障——为什么为「客户端断线」设计的重连恢复机制救不回一个所在 GPU 节点已经故障的会话？

## A zh
重连恢复机制之所以有效，是因为生成过程和它的 KV 缓存一直在一个健康的 GPU 节点上继续运行，不受客户端连接状态影响，所以重新连上的客户端只需要被交回已缓冲的输出和仍然存活的流。而当 GPU 节点本身宕机时，它持有的每一个会话的 KV 缓存都随之丢失——为每一个在飞会话都在多个节点间复制 KV 缓存，其代价会远高于它防范的这次故障本身，所以不这样做。这种情况下没有什么可以恢复：客户端的 SSE 流直接终止，服务只能提供一次全新的生成尝试，靠客户端的幂等键把它标记为一次新的尝试，而不是对一次已完成请求的重复提交。
