---
id: sproc-owners-vs-callers-rights
node: openplatform.stored-procedure-sandboxing
type: qa
tags: [grown]
---
## Q
Snowflake 存储过程的所有者权限（owner's rights）与调用者权限（caller's rights）有什么区别？各适合什么场景？

## A
所有者权限（默认）：过程以所有者角色的权限执行，调用者只需有该过程的 USAGE 就能完成过程内的操作，适合把受控的敏感操作（如清理某张表）委托给低权限用户，而不必直接授予他们表权限；为防止权限被滥用，这类过程读不到调用者的会话变量，也有部分会话操作受限。调用者权限（`EXECUTE AS CALLER`）：以调用者当前角色的权限执行，能使用调用者的会话上下文，适合只是把一串 SQL 自动化、不应给调用者带来额外权限的工具型过程。
