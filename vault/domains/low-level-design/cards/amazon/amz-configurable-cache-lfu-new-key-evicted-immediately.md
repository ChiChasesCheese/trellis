---
id: amz-configurable-cache-lfu-new-key-evicted-immediately
node: amazon.amz-configurable-cache
type: qa
step: 9
tags: [grown]
---
## Q
在可配置缓存里，LFU 实现最常见的错误是什么？

## A
先登记新 key、再选受害者。新 key 的频率是 1，通常是最小的，于是刚写入的 key 当场被淘汰。例：容量 1，put a、get a、put b，错误实现里 b 一写就被淘汰，`get(b)` 返回 None。修法：选受害者发生在新 key 登记之前（本设计先 `victim()`、再 `on_insert`），受害者只会是已有的 key。
