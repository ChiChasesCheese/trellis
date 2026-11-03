---
id: hi-sd-fb-post-search-6-phrase
node: sd.problem-breakdowns.fb-post-search.exam
type: qa
step: 6
---
## Q
**多关键词与短语查询**｜系统设计 · 题目拆解

帖子搜索要支持“Taylor Swift”这样的多词短语。请比较“集合求交再过滤”和“二元词组（bigram / shingle）索引”，说明各自的代价。

## A
**求交再过滤（可以）。** 取“Taylor”和“Swift”各自的帖子 ID，取交集，再读出帖子内容确认确实含有连续短语，排除“My friend Taylor made a swift exit”之类。缺点：两个 ID 集合可能各有上百万条，传输和求交都很重，难以满足 500 ms；若两个词常同时出现但不相邻，要过滤掉大量结果。

**二元词组索引（更好）。** 写入时把相邻两词当作一个键，如“Taylor Swift”，查询直接取这一项的帖子 ID，免去求交。

**代价。** 二元词组很稀疏，索引键从约 1000 万个单词变成 1 亿以上，存储暴涨。折中：只为可能被搜的词组建索引（可用 Count-Min Sketch 等概率结构统计词频），没有对应项时回退到求交。
