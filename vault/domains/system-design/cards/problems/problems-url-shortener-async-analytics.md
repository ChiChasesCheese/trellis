---
id: problems-url-shortener-async-analytics
node: problems.foundations.url-shortener
type: qa
step: 5
tags: [grown]
---
## Q
In a URL shortener design with a 100:1 read-to-write ratio, why would synchronously incrementing a click_count column in the primary database on every redirect be a design mistake, and what should happen instead?

## A
Doing it synchronously turns every redirect — the high-QPS read path — into a write against the primary store, forcing the primary database to absorb the full 100:1 read volume as writes and defeating the point of separating a low-QPS write path from a high-QPS read path. Instead, the redirect service should fire an async click event to a message queue after already returning the 302 to the client, and a downstream stream aggregator should batch-increment counts on a fixed window (e.g., every minute), accepting eventually-consistent click counts in exchange for keeping redirect latency independent of the analytics pipeline.

## Q zh
在一个读写比为 100:1 的短链接设计中，为什么在每次重定向时同步地对主数据库中的 click_count 列做自增会是一个设计错误？应该怎么做？

## A zh
同步自增会把每一次重定向——也就是高 QPS 的读路径——都变成对主存储的一次写入，等于让主数据库承受全部 100:1 的读流量作为写流量，抵消了把低 QPS 写路径和高 QPS 读路径分离开的意义。正确做法是重定向服务在已经向客户端返回 302 之后，异步地把一条点击事件发送到消息队列，由下游的流式聚合器按固定时间窗口（例如每分钟）批量地做增量写入，用「点击计数最终一致」换取重定向延迟不依赖分析管道。
