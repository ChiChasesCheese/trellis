---
nodes: [problems.commerce.payment-system]
url: https://www.uber.com/us/en/blog/high-throughput-processing/
---
# Building High Throughput Payment Account Processing

值得读：Uber 官方工程博客披露了单个高频账户写入速率超过单行锁上限时的真实解法——把
250 毫秒时间窗口内对同一账户的全部操作合并成一次原子读改写,批内单次操作摊销到
8–20 毫秒,不随批大小增加数据库往返次数,由此把单账户吞吐从逐个同步处理撑不住的量级
推到 30+ 次/秒。与本题解不同的地方在于：本题解把这组数字用在"平台手续费账户"这个更
具体的场景上,并额外论证了为什么本设计的手续费账户选择了更简单的无锁异步方案,而把
这篇文章描述的批处理留给"必须维持实时强一致余额的具体高频账户"这一更窄的场景。
