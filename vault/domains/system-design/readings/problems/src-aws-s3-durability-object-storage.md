---
nodes: [problems.foundations.object-storage]
url: https://docs.aws.amazon.com/AmazonS3/latest/userguide/DataDurability.html
tags: [no-archive]
---
# Data protection in Amazon S3

值得读：AWS 官方文档原文表述"设计为在一年内提供 99.999999999% 耐久性和 99.99%
可用性"，并说明标准存储类跨至少 3 个可用区冗余存储、设计为能承受整个可用区丢失。
题解「深入探讨」第 3 节引用这个数字作为真实系统达到的耐久性量级，并明确区分于
题解自己用简化二项分布模型算出的、量级低得多的条带丢失概率——两者不是同一个东西，
差距的原因（持续修复窗口远小于一年、跨故障域隔离）在正文中说明。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DataDurability.html)
%% trellis:end %%
