---
id: hi-c-sd-change-data-capture-n03-cdc-record
node: sd.deep-dives.change-data-capture.notes
type: qa
step: 3
---
## Q
**变更数据捕获 · 一条 CDC 记录长什么样**｜摘要 · 必会

一条 CDC 变更记录包含哪些部分？各自给消费者什么信息？

## A
- **操作类型：** 插入、更新还是删除，消费者据此决定怎么处理。
- **变更前镜像（before）：** 修改前的旧值，例如订单状态是 PROCESSING。
- **变更后镜像（after）：** 修改后的新值，例如 SHIPPED。
- **来源偏移（offset）：** 这次变更在数据库日志里的位置，如 Postgres 的 LSN（日志序列号）。CDC 系统靠它记录进度，重启后能从正确位置继续。
- **表名等元数据：** 指明变更的是哪张表。格式因数据库和工具不同，但核心结构大同小异。
- **消费者怎么用：** 搜索服务刷新对应文档；数仓管道把同一条变更导入分析表。
