---
id: bagu-link-dropbox-1-map
node: links.dropbox
type: qa
step: 1
---
## Q
**文件存储（Dropbox） · 会被追问哪些八股**｜必会

设计文件存储（Dropbox）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 文件字节和元数据分开，难点是大文件分块续传与多设备同步。基础是：元数据的事务存储、TCP 跨洋吞吐与并行连接、零拷贝下载、磁盘 IO 并发、资源泄漏监控、一致性哈希放块。

**下钻路线。**
- 文件元数据放哪个库 → InnoDB 事务让目录项与版本一次提交，[[b.mysql.exec-flow-engines|一条 SQL 的执行流程与存储引擎]]
- 跨洋上传为什么慢 → 单连接窗口爬得慢，分块并行加就近接入点，[[b.net.tcp-reliability|TCP 可靠传输、滑动窗口与拥塞控制]]
- 下载大文件 → Page Cache 加 sendfile 零拷贝，[[b.net.io-pagecache-zerocopy|文件 I/O]]
- 分块落盘并发 → 阻塞系统调用会占住线程，要限制磁盘 IO 并发，[[a.runtime.go-gmp|Go 的 GMP 调度模型]]
- 上传下载服务长跑 → CLOSE_WAIT 堆积就是连接没关，提前监控，[[a.net.time-wait-close-wait|TIME_WAIT 与 CLOSE_WAIT]]
- 多设备同步变更 → WebSocket 推送，客户端再按游标轮询兜底，[[a.net.websocket-push|消息推送]]
- 分块放到哪台存储 → 一致性哈希加虚拟节点，增删节点少搬数据，[[b.distributed.consistent-hashing|一致性哈希与虚拟节点]]
- 块的多副本和故障修复 → 异步复制会丢，要校验修复，[[b.scenario.distributed-kv|分布式 KV / 分布式缓存 / 文件存储设计]]

**业务场景。** 创作者在弱网下上传 4K 视频，断了要从已传的块续传，已传块用哈希校验，不能整个文件重来。
**系统设计。** [[links.youtube|视频平台（YouTube）]]：同样分块续传，后面接转码流水线；分布式文件系统（不可变文件、可变目录）：同样元数据与块分开，重点在元数据副本一致。
