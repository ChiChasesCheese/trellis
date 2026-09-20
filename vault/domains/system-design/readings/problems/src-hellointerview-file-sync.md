---
nodes: [problems.media.file-sync]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox
tags: [no-archive]
---
# Design Dropbox

值得读：Hello Interview 给出了这道题最完整的免费题解框架——分块与断点续传、presigned
URL 直传对象存储、内容定义分块（content-defined chunking）作为增量同步的优化点，并
按 mid/senior/staff 分层写出面试官对每个深度的期望。它把 CDC 作为一个笼统的"高级优化"
提出，没有展开固定分块和 CDC 各自的量化收益。本题解与它不同的地方在于：用具体的块数
和触发比例算出了 25 倍的带宽节省，并论证了按文件大小/类型分流两种分块策略，而不是无
差别全部换成 CDC（见本题解「深入探讨」第 1 节）。
