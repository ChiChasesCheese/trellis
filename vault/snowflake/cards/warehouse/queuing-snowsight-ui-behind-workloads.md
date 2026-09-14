---
id: queuing-snowsight-ui-behind-workloads
node: warehouse.query-queuing
type: qa
source: snowflake-docs
---
## Q
大账户里 Snowsight 的 Data Preview、Task Run History 等页面时快时慢，原因常常是什么？怎么解决？

## A
这些页面需要在仓库上运行 SQL 才能显示元数据以外的内容。若所选虚拟仓库（virtual warehouse）临时过载，界面发出的查询会排在其他活跃工作负载后面等待，导致页面忽快忽慢。解决办法是检查该仓库是否过载，换一个利用率较低的仓库；活跃用户多的大账户可为界面类查询专门配一个 X-Small 仓库。可在 Query History 中勾选 Client-generated statements 查看这些界面查询。
