---
id: amz-file-watcher-objects-and-their-jobs
node: amazon.amz-file-watcher
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，应有哪几个对象？各自只负责什么？

## A
`Stat`：文件指纹（mtime_ns、size）。`Event`：一次变化（种类 + 路径），订阅者靠它更新自己。`FileSystem`：协议，只有 `scan(root, recursive)` 一个方法，真实磁盘与测试假实现各一个。`diff`：纯函数，两张快照进、事件列表出。`Watcher`：持有已提交的快照、订阅表、后台线程，只有 `poll()` 推进。切分依据：读磁盘、比对、回调的变化原因不同。
