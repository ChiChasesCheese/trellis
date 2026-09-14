---
nodes:
- pruning.search-optimization-service
title: 搜索优化服务(Search Optimization Service)
corpus: snowflake-docs
section: 10-search-optimization-service
url: https://docs.snowflake.com/en/user-guide/search-optimization-service
tags:
- canonical
---

# 搜索优化服务(Search Optimization Service)

搜索优化服务专门加速非聚簇列上的高选择性点查,原理是维护一份持久化的搜索访问路径(search access path),记录每个微分区里可能出现哪些列值,从而在扫描前就跳过不可能命中的微分区——它不是 B 树索引,而是一种元数据加速结构。开启后由后台维护服务负责构建和增量更新访问路径,构建完成前查询不会被加速,数据更新时访问路径也会自动追平,期间查询仍返回正确结果但可能变慢。该服务对用户完全透明、无需额外仓库,但会产生存储和维护计算的双重成本。适用场景包括精确点查、文本/IP 搜索、子串与正则匹配、以及半结构化列上的等值与包含谓词查询。
