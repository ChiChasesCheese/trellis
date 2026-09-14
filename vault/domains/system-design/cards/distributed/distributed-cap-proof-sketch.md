---
id: distributed-cap-proof-sketch
node: distributed.cap
type: cloze
---
CAP proof sketch: partition two replicas, write `x=1` on one side, read `x` on the other. If the read side answers without hearing from the writer's side it may return {{c1::stale data — violating linearizability (sacrifices C)}}; if it waits or refuses until the partition heals it is {{c2::unavailable for that request (sacrifices A)}}. There is no third option, because the only way to know about the write is {{c3::a message across the very link that is down}}.

## zh
CAP 的证明梗概：让两个副本之间发生 partition，在一侧写 `x=1`，在另一侧读 `x`。如果读的一侧不等写入方的消息就作答，它可能返回{{c1::旧数据——违反 linearizability（牺牲 C）}}；如果它一直等待、或者直接拒绝，直到 partition 恢复，那它对这个请求就是{{c2::不可用的（牺牲 A）}}。没有第三条路，因为想知道这次写入，唯一的途径就是{{c3::一条必须穿过那条已经断掉的链路的消息}}。
