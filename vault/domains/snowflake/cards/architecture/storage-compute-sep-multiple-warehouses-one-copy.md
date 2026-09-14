---
id: storage-compute-sep-multiple-warehouses-one-copy
node: architecture.storage-compute-separation
type: qa
source: snowflake-docs
---
## Q
为什么在 Snowflake 中，可以让多个不同用途（如 ETL、BI 报表）的虚拟仓库同时访问同一批业务数据而互不干扰？

## A
因为业务数据只有一份，持久化保存在与计算完全分离的存储层；各个虚拟仓库只是分别从这一份共享数据之上读取所需内容，彼此之间没有共享的计算资源，也不需要各自维护一份数据副本。这使得为不同工作负载单独开一个虚拟仓库、而不必担心数据不一致或负载互相拖累成为可能。
