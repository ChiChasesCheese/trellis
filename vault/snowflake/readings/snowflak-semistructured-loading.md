---
nodes:
- semistructured.variant-type-storage
- semistructured.schema-on-read-parsing
title: 半结构化数据的加载与内部表示(VARIANT/ARRAY/OBJECT)
corpus: snowflake-docs
section: 17-semistructured-intro
url: https://docs.snowflake.com/en/user-guide/semistructured-intro
tags:
- canonical
---

# 半结构化数据的加载与内部表示(VARIANT/ARRAY/OBJECT)

JSON、Avro、ORC、Parquet 等半结构化数据没有固定 schema、可以任意嵌套,Snowflake 用 VARIANT(可容纳任意类型的容器)、ARRAY、OBJECT 三种类型搭建层级结构:VARIANT 可以装 ARRAY 或 OBJECT,ARRAY/OBJECT 内部的值又都是 VARIANT。加载时,只要指定了 Snowflake 能识别的格式,数据会在加载这一刻就被解析成这套内部优化的列式表示,而不是原样存成大文本字段;这就是 schema-on-read 的含义——不必提前知道字段结构就能加载,查询时再按路径表达式取出所需字段。读完应理解:半结构化数据在存储层面已经和结构化数据共享同一套微分区格式,只是多了一层路径寻址。
