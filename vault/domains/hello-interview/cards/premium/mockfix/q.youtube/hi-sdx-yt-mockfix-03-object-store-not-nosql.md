---
id: hi-sdx-yt-mockfix-03-object-store-not-nosql
node: sd.problem-breakdowns.youtube.more
type: qa
step: 103
---
## Q
**原片存哪：对象存储，不是数据库**｜模拟面试补强 · 视频平台（YouTube）

面试官：「百兆级的原始视频，你放 NoSQL 里对吗？」

## A
**一句话。** 大二进制放对象存储（S3/GCS），数据库只存元数据和对象 key；两者靠 video_id 关联。

**要点。**
- 为什么不放数据库？：单行大小有上限，复制和备份都按字节算，读写把数据库带宽打满。
- 对象存储给了什么？：近乎无限容量、11 个 9 的持久性、按量计费、能直接做 CDN 源站。
- 元数据放哪？：标题、作者、状态、各档位的对象 key 放 SQL，按 video_id 查。

**常见失分。**
- 先说 NoSQL 存原片，被追问才改成对象存储：字节和元数据分层要第一时间说出来。
