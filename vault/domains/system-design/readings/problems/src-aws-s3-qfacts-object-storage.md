---
nodes: [problems.foundations.object-storage]
url: https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html
tags: [no-archive]
---
# Amazon S3 quick facts (multipart upload core specifications)

值得读：AWS 官方文档，列出对象存储真实系统的硬性数字：单对象最大 48.8TiB、
multipart 单次上传最多 10,000 个分片、分片大小 5MiB–5GiB、单次 ListParts/
ListMultipartUploads 最多返回 1,000 条。题解「深入探讨」第 4 节（multipart 上传）
的算术直接采用这些数字；第 5 节列举十亿级 key 的桶用到的"ListObjectsV2 单页最多
1,000 个 key"来自 [ListObjectsV2 API 参考](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html)
这个独立页面，不是本页。
