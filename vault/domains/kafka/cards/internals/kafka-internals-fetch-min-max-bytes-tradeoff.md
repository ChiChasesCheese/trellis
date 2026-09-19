---
id: kafka-internals-fetch-min-max-bytes-tradeoff
node: internals.request-handling
type: qa
step: 6
source: kafka-2e
---
## Q
消费者可以给一次获取请求（fetch request）同时设置「最多返回多少数据」和「至少凑够多少数据才返回」两个参数。为什么需要同时设置这两个看似相反的限制？

## A
上限（最多返回多少数据）是为了防止 broker 一次性塞进大量数据把消费者的内存撑爆——客户端要为返回的数据预留内存，没有上限就存在被撑爆的风险。下限（比如设成 10 KB）则是为了在主题流量不大时减少来回请求的次数：如果不设下限，消费者可能每隔几毫秒就发一次请求却常常拿到很少甚至没有数据，浪费 CPU 和网络开销；设了下限后，broker 会把响应留在炼狱（purgatory）里，等凑够数据（或等到客户端设定的超时时间）再一次性返回，总数据量不变但往返次数更少。
