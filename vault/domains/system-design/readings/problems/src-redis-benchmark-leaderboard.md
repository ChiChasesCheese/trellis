---
nodes: [problems.realtime.leaderboard]
url: https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/benchmarks/
---
# Redis benchmark (redis-benchmark and Redis's single-threaded architecture)

值得读：官方明确说明 Redis 对命令执行是单线程的，"不为利用多核设计"，多核扩展要靠
多开实例而不是指望一个实例吃满多核；同时给出无流水线条件下单实例简单命令（`SET`）
能跑到十几万 QPS 量级的数字，以及流水线能进一步大幅提升合成基准吞吐、但生产环境的
持久化/复制/监控开销会显著拉低实际可持续吞吐这一告诫。本题解「深入探讨」第 1 节
"先算清楚要不要分片，而不是默认要分片"这一论点直接依据这份文档给出的基线数量级；
本题解采用的单节点可持续上限（约 50,000 op/s）是在这个基线上打五折（为有序集合
O(log N) 操作和生产开销留出余量）得到的工程假设，文中已明确标注，不是文档给出的
精确数字，与本知识库姊妹题 rate-limiter 对同一数量级操作采用的假设方向一致。
