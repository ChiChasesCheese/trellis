---
id: sproc-filesystem-tmp-only
node: openplatform.stored-procedure-sandboxing
type: qa
tags: [grown]
---
## Q
存储过程或 UDF 的代码需要写一个中间文件，能写到节点的任意路径吗？需要持久保存的文件应该放在哪里？

## A
不能。沙箱限制文件系统访问，代码通常只能写入临时目录（如 `/tmp`），这里的文件只在本次执行期间存在、执行结束后不保证保留，也不会在节点之间共享。需要读取的依赖文件或需要持久保存的输出应放在 stage（Snowflake 管理的文件暂存区）中，通过 Snowpark session 的文件读写 API 或 `IMPORTS` 子句访问，这样文件的访问同样受 RBAC 权限控制。
