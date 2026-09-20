---
nodes: [problems.search.news-aggregator]
url: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/33026.pdf
---
# Detecting Near-Duplicates for Web Crawling

值得读：Manku、Jain、Sarma 在 Google 发表于 WWW 2007 的第一方论文，披露了在 80 亿网页
规模上用 64 位 SimHash 指纹（比 Broder 式 shingle 指纹的 24 字节/文档小得多）配合汉明
距离 k=3 判重的生产实践，以及用多张按位置换排序的表解决"在线查询几毫秒内完成、批量查询
单日十亿级吞吐"这个汉明距离问题的具体设计参数（例如 20 张表在 8B 规模下把每次探测候选数
压到约 8）。本题解「深入探讨」第 2 节直接采用了论文描述的分表方法，但按本设计自己 720
万篇活跃文章的规模重新计算出 15 张表、候选数约 1.7 这组参数——这组具体数字是本题解基于
论文方法的计算，不是论文本身给出的（论文给出的参数是为 Google 自己 8B 页规模设计的）。
