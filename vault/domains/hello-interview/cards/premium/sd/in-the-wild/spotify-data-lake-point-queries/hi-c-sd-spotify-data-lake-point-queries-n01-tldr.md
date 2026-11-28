---
id: hi-c-sd-spotify-data-lake-point-queries-n01-tldr
node: sd.in-the-wild.spotify-data-lake-point-queries.notes
type: qa
step: 1
---
## Q
**Spotify 数据湖点查 · 全貌**｜摘要 · 必会

数据湖擅长扫描、不擅长查某一个人的数据。Spotify 想出了什么办法，而且不复制数据？

## A
- **背景：** 大公司把数据放在便宜的对象存储里（数据湖，data lake）：保留完整历史，不必配给容量，各团队读同一份数据。适合每周报表、模型训练这类大范围扫描；但"某用户听过什么"这种在线功能或 AI agent 要的点查很慢。
- **常见补救：** 把需要快的数据复制进 Bigtable、DynamoDB 或 Redis。代价是按 GB 付费，团队不得不限额配给。
- **Spotify 的办法：** 叫 RAP（Random Access Parquet）的外部索引，记录每个键的数据在哪个文件的哪几行，不改动数据文件；再配合写入侧改造，让同一个用户的数据挨在一起。
- **结果：** 同一份文件既供 BigQuery 周报扫描，也能回答单个用户的问题，成本约为一次存储读取。
- **启示：** 在"全湖扫描"和"全量复制进 KV 存储"之间有第三条路。
