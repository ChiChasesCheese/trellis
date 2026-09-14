---
id: copy-into-no-dml-error-logging
node: ingestion.bulk-copy-into
type: qa
source: snowflake-docs
---
## Q
一张表开启了 DML 错误日志（`ERROR_LOGGING = TRUE`，把出错行记入错误表而不让语句失败），之后对它执行 `COPY INTO` 会怎样？COPY 的坏行会进入错误表吗？

## A
COPY INTO 会在编译阶段直接报错 `Error logging is not supported in statement 'COPY INTO'`。DML 错误日志只覆盖 INSERT、UPDATE、MERGE；COPY 和 Snowpipe 等摄取路径上的失败不会记入错误表，文件加载中的坏行需要用 COPY 自己的 `ON_ERROR` 等错误处理选项来控制。
