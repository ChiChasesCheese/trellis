---
id: hl-fit-d7-networking
node: company.fit
type: qa
step: 19
---
## Q
JD 日常工作 "Improve networking communication between different components of the system to achieve optimal latency and throughput"，你没调过网络时怎么回答？

## A
评级：**缺口**。唯一相关：Kafka 批量消费（批量 vs 延迟的取舍）；没有 socket / TCP / 序列化 / 零拷贝的亲手经验。

说法："I haven't tuned network paths. What I understand: latency vs throughput trade through batching, Nagle's algorithm, serialization cost. I'd start by measuring where the time goes." 然后问对方当前的瓶颈。

要补：TCP / UDP、Nagle、NIO、组播与内核旁路；虚拟线程。
