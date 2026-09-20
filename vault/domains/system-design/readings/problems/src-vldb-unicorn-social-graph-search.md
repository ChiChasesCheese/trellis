---
nodes: [problems.social.social-graph-search]
url: https://www.vldb.org/pvldb/vol6/p1150-curtiss.pdf
---
# Unicorn: A System for Searching the Social Graph

值得读：VLDB 2013 论文，把社交图谱建模成按边类型和源节点 ID 组织的倒排索引，按结果 ID
（而不是按查询词）分片以在个别机器故障时优先返回部分结果，披露了数十亿节点、万亿级边、
每天数十亿次查询、简单查询平均约 11ms 延迟的真实规模。本题解直接采用了它"类型化边即倒排索引词项"
的建模方式，但没有实现它完整的多阶段聚合算子集合，因为本题范围内的查询不需要那种通用的
组合查询能力。
