---
id: isolation-read-consistency-mode-global
node: txn.snapshot-isolation
type: qa
source: snowflake-docs
---
## Q
会话 1 插入一行并立即查到了它，几乎同时会话 2（在插入之前就已建立）执行同样的查询却没看到这一行。这是 bug 吗？有哪些办法让两个会话结果一致？

## A
不是 bug。默认的 `READ_CONSISTENCY_MODE = 'SESSION'` 只保证单个会话内部的读一致性，近乎并发运行的其他会话可能暂时看不到新提交。按推荐顺序的解决办法：1) 让相互依赖的查询在同一个会话里执行；2) 在会话 1 提交之后再启动会话 2；3) 由 ACCOUNTADMIN 在账户级把 `READ_CONSISTENCY_MODE` 设为 `'GLOBAL'`，代价是查询响应多出通常为毫秒级的延迟。
