---
nodes:
- openplatform.hybrid-tables-oltp
title: 混合表(Hybrid Table):行存与点查/高并发写
corpus: snowflake-docs
section: 31-tables-hybrid
url: https://docs.snowflake.com/en/user-guide/tables-hybrid
tags:
- canonical
---

# 混合表(Hybrid Table):行存与点查/高并发写

混合表是专为低延迟、高吞吐的点查和高并发写设计的表类型,底层用行存(row store)作为主存储、支持行级锁,并强制主键、外键、唯一约束等在标准表上通常是可选甚至不生效的完整性约束。它与标准表共用同一套云服务层做查询编译优化、同一套查询引擎和虚拟仓库执行——可以直接和标准表 JOIN,也可以对混合表与标准表做同一个原子事务,无需自己实现两阶段提交。数据写入行存后会异步复制到列式对象存储,供大范围分析扫描使用而不影响在线读写。因为主存储是行存,混合表的压缩率和存储体积通常比标准表大,选型时要按点查/写为主还是分析扫描为主来决定用哪种表。
