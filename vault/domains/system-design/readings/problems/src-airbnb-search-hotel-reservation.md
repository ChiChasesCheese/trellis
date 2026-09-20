---
nodes: [problems.commerce.hotel-reservation]
url: https://medium.com/airbnb-engineering/embedding-based-retrieval-for-airbnb-search-aabebfc85839
tags: [engineering-blog]
---
# Embedding-Based Retrieval for Airbnb Search

值得读：Airbnb 自己的搜索检索团队指出房源"价格与可用性数据频繁更新"这一约束直接影响了检
索层索引结构的选型——为控制频繁更新下的内存占用，他们在 HNSW 和 IVF 之间选择了后者。本题
没有采用同等复杂度的向量检索方案，但复用了同一个结论支撑搜索索引只能存粗粒度信号（而非精
确库存数字）这一设计决策；和多数只讲排序模型本身的题解文章不同，这篇的价值在于点出了"索引
更新频率"本身是一个要显式权衡的设计变量。
