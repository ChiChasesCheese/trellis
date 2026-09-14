---
id: distributed-consistency-ladder
node: distributed.consistency
type: cloze
---
The consistency ladder, strongest to weakest, and what each rung gives up: **linearizability** promises {{c1::every operation sees the effects of all operations completed before it in real time — one up-to-date copy}}, and is the only rung that {{c2::cannot stay available during a network partition (must stall or refuse)}}. One step down, **causal consistency** keeps {{c3::the order of operations that depend on each other (read-then-write, same session chains), while letting concurrent operations be seen in different orders on different nodes}}. Below it, **session guarantees** (read-your-writes, monotonic reads) protect {{c4::only one client's view of its own interactions, promising nothing across clients}}. The bottom rung, **eventual consistency**, promises only {{c5::convergence at some unspecified time — no recency bound, and reads may go backwards meanwhile}}.

## zh
一致性阶梯，从最强到最弱，以及每一级放弃了什么：**linearizability（线性一致性）**承诺{{c1::每个操作都能看到真实时间中先于它完成的所有操作的效果——如同只有一份最新副本}}，它也是唯一一级{{c2::在网络分区期间无法保持可用（必须停顿或拒绝服务）}}的。往下一级，**causal consistency（因果一致性）**保住{{c3::相互依赖的操作之间的顺序（先读后写、同一会话的链条），但允许并发操作在不同节点上以不同顺序被看到}}。再往下，**session guarantees（会话保证，如 read-your-writes、monotonic reads）**只保护{{c4::单个客户端对自己交互的视图，对跨客户端不作任何承诺}}。最底一级，**eventual consistency（最终一致性）**只承诺{{c5::在某个不确定的时刻收敛——没有新鲜度上界，期间读还可能倒退}}。
