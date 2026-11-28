---
id: hi-pt-distributed-file-system-8-path-cache
node: qb.sd.distributed-file-system.points
type: qa
step: 8
---
## Q
**分布式文件系统 · 路径解析缓存**｜追问 · 出自：分布式文件系统 › 深入 4

分布式文件系统里深度为 d 的路径要 d 次目录项查找，可能跨分片。怎样缓存？目录可变，缓存怎么失效？

## A
**做法。** 网关缓存（租户、路径前缀）到 dirId 的映射。

**失效。** 目录可变，所以带目录版本号或短过期（如 1 秒），删除和改名时按前缀清除。

**可永久缓存。** fileId 对应的块列表永不变。
