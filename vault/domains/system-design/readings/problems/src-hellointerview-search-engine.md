---
nodes: [problems.search.search-engine]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-post-search
tags: [no-archive]
---
# Design Facebook Post Search

值得读：Hello Interview 对站内帖子搜索这道题给出了完整的需求切分（按关键词搜索、按时间/
点赞数显式排序）和一套具体实现（Redis 倒排索引、按时间序的 list 和按点赞数的 sorted set
两套并行索引、点赞更新按里程碑批处理、查询时过取候选再用新鲜计数精排）。与本题解不同的
地方在于：本题解把里程碑批处理的写放大下降幅度用对数公式具体算了出来（一条最终获赞 10
万的帖子约降低 5,882 倍），并把分片策略从"选用什么现成存储"延伸到了"按文档分片还是按
词项分片"这个更底层、和语料规模及词频倾斜强相关的问题，这一层原文没有展开。
