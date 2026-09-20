---
nodes: [problems.social.social-graph-search]
url: https://github.com/twitter-archive/flockdb
---
# Twitter — FlockDB

值得读：Twitter 开源的图存储，同样把边存成正向和反向两行，披露了 2010 年 4 月的真实
生产数字（130 亿条边、峰值 2 万写/秒、10 万读/秒）。本题解与它的区别在于：FlockDB 明确
不支持多跳遍历（文档里写明这是非目标），而多跳的最短路径查询正是本题解的核心难点之一，
本题解必须在 FlockDB 划定的范围之外单独设计这一部分。
