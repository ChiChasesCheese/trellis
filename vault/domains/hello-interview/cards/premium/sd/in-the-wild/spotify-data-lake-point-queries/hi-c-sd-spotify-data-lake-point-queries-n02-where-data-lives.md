---
id: hi-c-sd-spotify-data-lake-point-queries-n02-where-data-lives
node: sd.in-the-wild.spotify-data-lake-point-queries.notes
type: qa
step: 2
---
## Q
**Spotify 数据湖点查 · 数据湖是什么、好在哪**｜摘要 · 必会

数据湖指什么？它为什么受欢迎，查询是怎么跑的？

## A
- **定义：** 事件（如每首歌的播放）最终以文件形式放在对象存储（GCS、S3）里，不是数据库的行。像一座大而便宜的档案库。
- **怎么查：** 分析师用 Trino、BigQuery 这类查询引擎，直接在原地读文件，不先装进数据库；机器学习流水线也读同样的文件。都是大范围扫描，而不是 Postgres 那种点查。
- **好处：** 每 GB 便宜得多，所以 Spotify 能在 GCS 里存 EB 级的全部历史，不用只留最近一段；所有工具读同一份文件，只有一份"真相"。
- **代价：** 在线的点查要求（请求返回之前就要答案）满足不了。
