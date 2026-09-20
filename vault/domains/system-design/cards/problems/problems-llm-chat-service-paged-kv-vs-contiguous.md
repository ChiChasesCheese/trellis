---
id: problems-llm-chat-service-paged-kv-vs-contiguous
node: problems.realtime.llm-chat-service
type: qa
step: 3
tags: [grown]
---
## Q
In a chat service where conversations range from a few tokens to several thousand tokens of context, why does allocating each conversation's KV cache as one contiguous block of GPU memory (that grows as the conversation grows) waste capacity even when the total free memory is sufficient, and what's the standard fix?

## A
Contiguous allocation requires a single unbroken span of free memory large enough for the request; as conversations of different lengths start and finish, the freed gaps between them end up scattered in sizes that don't line up with what a new, growing conversation needs next — external fragmentation — so a GPU can be unable to admit a new session even though the sum of its free memory would be more than enough. The fix, used by PagedAttention/vLLM-style serving, is to allocate KV cache in small fixed-size blocks that don't need to be physically contiguous, the same idea as virtual-memory paging in an OS: a conversation's KV cache is a list of blocks scattered wherever space is free, eliminating the fragmentation problem and letting memory utilization approach the theoretical capacity.

## Q zh
在一个会话上下文从几个 token 到几千 token 不等的聊天服务里，为什么把每个会话的 KV 缓存分配成一块随会话增长而扩大的连续 GPU 内存，即便总空闲显存足够，也会浪费容量？标准的解决办法是什么？

## A zh
连续分配要求有一整段足够大的、不间断的空闲内存来满足请求；随着长度不同的会话陆续开始和结束，它们释放出的空隙大小参差不齐，往往和下一个正在增长的会话需要的大小对不上——这就是外部碎片——于是即使空闲显存总量绰绰有余，GPU 也可能无法容纳一个新会话。标准的解决办法（PagedAttention/vLLM 一类服务系统采用）是把 KV 缓存分配成不要求物理连续的小块固定大小的 block，和操作系统虚拟内存分页是同一个思路：一个会话的 KV 缓存是散落在任意空闲位置的一组 block 列表，从而消除碎片问题，让内存利用率逼近理论容量。
