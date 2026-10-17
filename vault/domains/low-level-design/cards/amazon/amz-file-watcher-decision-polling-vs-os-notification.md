---
id: amz-file-watcher-decision-polling-vs-os-notification
node: amazon.amz-file-watcher
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，用轮询比对快照还是用系统通知（inotify 等）？选了轮询之后怎样保留换实现的余地？

## A
系统通知延迟低、不耗 CPU，但各平台接口不同、标准库没有、不能在白板上手写；轮询只用标准库、行为一致，代价是延迟等于轮询间隔并要遍历目录。选轮询，同时把读文件系统藏在 `FileSystem.scan` 后面：以后挂上通知实现，比对、订阅、去抖都不动。
