---
id: hl-cache-read-sharing-ok
node: foundations.cpu-cache-locality
type: qa
step: 27
---
## Q
多个线程只读同一个缓存行会有伪共享问题吗？由此得到什么并发设计原则？

## A
没有问题。多个核都只读同一行时，每个核持有 Shared 副本，不会互相失效；问题出在**有写者**。

所以「不变对象 + 多线程读」是对缓存最友好的并发设计；共享可写数据的线程越多越易乒乓，每个线程只写自己的行最快。
