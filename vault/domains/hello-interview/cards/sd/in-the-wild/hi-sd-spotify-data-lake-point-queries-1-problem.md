---
id: hi-sd-spotify-data-lake-point-queries-1-problem
node: sd.in-the-wild.spotify-data-lake-point-queries
type: qa
step: 1
---
## Q
**数据湖擅长扫描，不擅长点查**｜系统设计 · 业界案例

Spotify 把 EB 级数据放在对象存储里的 Parquet 文件中（数据湖）。为什么这种布局回答「某个用户听了什么」特别慢，而回答「各国平均收听时长」却很快？

## A
**要点。** Parquet 按列存储：同一列的值挤在一起，再切成行组（row group）、页（page），文件末尾有 footer 描述位置。同列值相似，压缩效果好；引擎还能整页跳过不需要的数据。算「各国平均时长」只要读两列，正好是它擅长的大范围扫描。

查某一个用户，只是散落在许多文件里的几百字节，却要把整页（可达约 4 MB）读下来；查询引擎（Trino、BigQuery）还要为这一行排一个完整的分布式分析作业。

**为什么。** 对象存储本身不慢：GCS 一次请求约 30 到 100 ms，新一代层级可到个位数毫秒；慢在读之外包裹的那一堆东西。

**取舍。** 常规做法是把要快的数据复制进 Bigtable、DynamoDB 或 Redis，按 GB 计费，团队不得不限额配给，其余数据留在湖里却无法在线服务。
