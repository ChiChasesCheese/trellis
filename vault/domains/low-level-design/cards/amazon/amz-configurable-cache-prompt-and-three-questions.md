---
id: amz-configurable-cache-prompt-and-three-questions
node: amazon.amz-configurable-cache
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「可配置缓存（Configurable Cache）」怎么问的？开场先问哪三个澄清问题？

## A
报告的原话：设计一个缓存，支持可插拔的淘汰策略（eviction policy，如 LRU、LFU）和可互换的存储后端（storage backend，如内存、文件；还提到 heap、stack）。先问三件事：(1) 策略与后端是创建时选定，还是运行时可换？决定要不要支持热切换；(2) 值是什么类型？文件后端要求能序列化，决定存储接口收不收任意对象；(3) 要不要过期、统计、线程安全？这几项各是一层可以后加的东西。
