---
id: principles-isp-trigger
node: principles.solid
type: qa
---
## Q
什么时候你知道你的接口违反了接口分离原则？

## A
触发器：
- 实现者强制实现它们不使用的方法
- 调用者只调用接口的一部分
- 接口名中有多个概念："Read-Write-Lock"、"Serializable-Comparable"
- 一个类有多个客户端需要不同的操作子集

症状：
- 模拟或存根会伪造不用的方法
- 测试中对实现者不相关的方法进行设置
