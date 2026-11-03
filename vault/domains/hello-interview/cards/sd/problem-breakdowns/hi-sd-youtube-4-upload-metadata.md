---
id: hi-sd-youtube-4-upload-metadata
node: sd.problem-breakdowns.youtube.exam
type: qa
step: 4
---
## Q
**YouTube：元数据存储与上传路径**｜系统设计 · 问题拆解

YouTube 的视频元数据存哪里、按什么分区？视频文件怎么上传？为什么不能只按键去想分区问题？

## A
**元数据。** 每天约 100 万个视频，一年约 3.65 亿条记录，需要能水平分区的库，选 Cassandra：高可用且能指定分区键。以 videoId 分区，因为只做单个视频的点查，不做批量访问。

**分区思路的三类系统。**
- 需要读取集中在少数节点的系统，要精心设计分区
- 需要在某个范围内保证一致性的系统，用分片的 ACID 关系库，如 Ticketmaster 按演出分片
- 像这里只做点查的系统，几乎不需要精心分区，按 videoId 分即可

**视频内容。** 和 Dropbox 一样，客户端用预签名 URL 以分段上传（multipart upload）直传 S3，后端不接触视频字节；上传接口因此改为请求预签名 URL。这是处理大文件（Handling Large Blobs）模式的典型例子。
