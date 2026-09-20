---
nodes: [problems.search.web-crawler]
url: https://www.cs.cornell.edu/courses/cs685/2002fa/mercator.pdf
tags: [paper]
---
# Mercator: A Scalable, Extensible Web Crawler

值得读：Heydon 与 Najork 的学术论文，是本题解 URL frontier 架构（前端队列做优先级、后端队
列做宿主隔离、按下次允许抓取时间排序的最小堆）的直接来源，也是"任意时刻至多一个 worker 对
一个宿主发起请求"这条礼貌约束的原始出处。本题解在论文架构的基础上补充了具体的容量数字（后
端队列数量应与 worker 并发度而不是宿主总数同量级），论文本身只给出架构，没有给出这类量化。
