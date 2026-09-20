---
nodes: [problems.foundations.object-storage]
url: https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html
tags: [no-archive]
---
# Best practices design patterns: optimizing Amazon S3 performance

值得读：AWS 官方文档，给出每个分区好的 key 前缀能扛 3,500
PUT/COPY/POST/DELETE 或 5,500 GET/HEAD 每秒、一个桶内前缀数量没有上限、以及
不再需要人为随机化前缀（S3 会按访问模式自动分区）的具体数字和说明。题解「容量
估算」和「深入探讨」第 5 节用这两个吞吐数字反推元数据分片数，但 512/4,096 这样
的具体分片规划是本题自己的设计选择，不是 AWS 的真实内部实现细节。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/optimizing-performance.html)
%% trellis:end %%
