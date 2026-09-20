---
nodes: [problems.search.top-k]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/top-k
tags: [no-archive]
---
# Top K Problem Breakdown

值得读：把"最多观看视频排行榜"从精确哈希表逐步升级到 Count-Min Sketch 的完整推理过程，
容量估算和 API 设计示例齐全。比本题多讲了 TimescaleDB/Druid/Pinot 这类实时 OLAP 引擎作为
落地选项；本题在此基础上补了 Space-Saving 的确定性候选保证，以及"按 item 分区 vs 按维度
分区"两种合并方式各自的正确性论证，这是它没有展开的部分。
