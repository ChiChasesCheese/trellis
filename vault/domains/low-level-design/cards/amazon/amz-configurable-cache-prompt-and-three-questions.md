---
id: amz-configurable-cache-prompt-and-three-questions
node: amazon.amz-configurable-cache
type: qa
step: 1
tags: [grown]
---
## Q
可配置缓存（Configurable Cache）要你设计什么？开场先问哪三个澄清问题？

## A
题目：设计一个缓存（容量有限，满了要扔掉一条旧的），支持可插拔的淘汰策略（eviction policy，缓存满时「扔谁」的规则，如 LRU 扔最久没碰的、LFU 扔次数最少的）和可互换的存储后端（storage backend，数据真正放的地方，如内存、文件；口头上还可能说 heap、stack）。先问三件事：(1) 策略与后端是创建时选定，还是运行时可换？决定要不要支持热切换；(2) 值是什么类型？文件后端要求能序列化，决定存储接口收不收任意对象；(3) 要不要过期、统计、线程安全？这几项各是一层可以后加的东西。
