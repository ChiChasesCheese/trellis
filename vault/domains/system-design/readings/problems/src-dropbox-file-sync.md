---
nodes: [problems.media.file-sync]
url: https://dropbox.tech/infrastructure/streaming-file-synchronization
tags: []
---
# Streaming File Synchronization

值得读：Dropbox 官方工程博客披露了文件按固定 4MB 分块、以 SHA-256 寻址的真实工程
实现细节，是本题解「需求」「容量估算」和「深入探讨」第 1 节里块大小数字的直接来源，
而不是猜测出来的。本题解在分块策略上与这篇文章的真实选择不同并明确标注了分歧：本
设计认为对大文件采用内容定义分块（CDC）更适合局部插入式编辑场景，固定分块只保留给
小文件和已压缩格式，这是本题解自己的设计取舍，不代表 Dropbox 的真实实现。
