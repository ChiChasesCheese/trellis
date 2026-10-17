---
id: amz-file-watcher-snapshot-diff-mtime-and-size
node: amazon.amz-file-watcher
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon 文件监听器设计里，快照 `路径 → (mtime_ns, size)` 怎么比出 CREATED、MODIFIED、DELETED？为什么指纹不能只有 mtime？

## A
新快照独有的路径是 CREATED，旧快照独有的是 DELETED，两边都有而指纹不同的是 MODIFIED。mtime 有时间粒度（有的文件系统是 1–2 秒），同一粒度内改两次，第二次 mtime 不变；加 size 后，mtime 同为 100、size 从 10 变 25 就能发现。剩余盲区：同一粒度内改成同样长度的内容，真实工具用 inode、ctime 或内容哈希补。
