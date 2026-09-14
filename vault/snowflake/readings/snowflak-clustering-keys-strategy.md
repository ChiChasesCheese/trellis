---
nodes:
- storage.clustering-keys
- storage.natural-vs-explicit-clustering
title: 聚簇键的选择与何时需要它
corpus: snowflake-docs
section: 03-tables-clustering-keys
url: https://docs.snowflake.com/en/user-guide/tables-clustering-keys
tags:
- canonical
---

# 聚簇键的选择与何时需要它

多数表靠插入顺序自然形成的聚簇(natural clustering)就已经够用;只有当表体积达到 TB 级、查询高选择性且集中在同几列上时,显式定义聚簇键(clustering key)才值得付出维护成本。文中给出选键策略:优先选高频出现在过滤谓词里的列,列数控制在 3–4 个以内,并按基数从低到高排序;基数过低裁剪不到位,基数过高又会推高重新聚簇(reclustering)的信用点消耗。判断要不要升级为显式聚簇,看的是聚簇深度(clustering depth)是否随时间劣化,而非拍脑袋决定。这是从只依赖自然顺序,到主动管理数据物理布局的分水岭。
