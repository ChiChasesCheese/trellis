---
nodes: [problems.search.metrics-monitoring]
url: https://prometheus.io/docs/introduction/faq/
---
# Prometheus – FAQ: Why do you pull rather than push?

值得读：Prometheus 官方 FAQ，第一方来源，给出拉模型的核心论据——采集端集中控制抓取频率
和目标配置的变更不需要重新部署被采集的服务，抓取失败本身就是"目标是否健康"的一等公民
信号。本题解「深入探讨」第 1 节采纳了这个论据作为默认采集路径的理由，但原文更多是原则性
论述加上"什么情况下才该用 Pushgateway"的简短说明；本题解额外补充了"为生命周期短于抓取
间隔的批处理作业保留一条独立推送通道，并把它当作已知的可用性/扩展性风险"这一具体设计
取舍，原文没有展开这条例外路径本身的架构含义。
