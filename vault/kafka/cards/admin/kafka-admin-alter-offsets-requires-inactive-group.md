---
id: kafka-admin-alter-offsets-requires-inactive-group
node: admin.consumer-group-ops
type: qa
source: kafka-2e
---
## Q
用 AdminClient 的 alterConsumerGroupOffsets（或命令行工具的偏移量重置功能）去修改一个消费者群组的偏移量时，为什么必须先确保这个群组里的所有消费者都已经关闭，否则操作可能失败或被覆盖？

## A
消费者只有在启动时或被重新分配到新分区时才会去读取已提交的偏移量，运行过程中并不会感知偏移量在外部被修改，所以如果群组还活跃，消费者会继续按自己内存里的位置提交偏移量，把刚刚外部写入的新偏移量覆盖掉。更严重的是，如果消费者群组仍处于活跃状态，群组协调器（group coordinator，负责管理群组成员和偏移量提交的 broker 组件）会认为这次外部修改偏移量的请求是「非群组成员」发起的，直接抛出 UnknownMemberIdException 异常，导致修改直接失败。因为没有专门的命令能「暂停」一个群组，唯一的办法是先把消费者应用程序整体关闭。
