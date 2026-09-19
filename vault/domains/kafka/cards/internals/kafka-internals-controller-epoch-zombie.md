---
id: kafka-internals-controller-epoch-zombie
node: internals.controller
type: qa
step: 3
source: kafka-2e
---
## Q
某个控制器（controller）因为一次很长的 JVM 垃圾回收（GC）停顿而与 ZooKeeper 失联，集群趁机选出了新控制器；停顿结束后，旧控制器恢复运行，但它并不知道新控制器已经存在，仍继续向其它 broker 发送指令。Kafka 用什么机制防止这种「僵尸控制器」造成的脑裂（split brain，两个节点同时认为自己是唯一控制器）？

## A
每当一个新控制器当选，都会通过 ZooKeeper 的条件递增操作获得一个严格更大的**epoch（选举代数，一个单调递增的整数）**，并把这个 epoch 带在自己发出的每条控制消息里。其它 broker 会记住当前已知的最大 epoch：一旦收到的消息里 epoch 比自己记录的小，就直接丢弃。这样，恢复过来的旧控制器发出的指令因为携带的是旧 epoch，会被所有 broker 忽略，即使它自己还不知道已经被取代，也无法再影响集群状态，从而避免了脑裂。
