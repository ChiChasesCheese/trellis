---
nodes: [problems.social.news-feed]
url: https://highscalability.com/the-architecture-twitter-uses-to-deal-with-150m-active-users/
---
# The Architecture Twitter Uses to Deal with 150M Active Users

值得读：披露了 Twitter 真实的 fan-out 服务细节——Redis 集群三副本、每个用户主时间线
（home timeline）上限 800 条、单次 pipeline 操作批量写入约 4,000 个目标、名人账号的
fan-out P99 延迟可达 5 分钟。本题解「容量估算」一节沿用了同样的 800 条上限作为假设，并
用这篇文章"几 TB 内存服务 1.5 亿活跃用户"的真实数字，交叉验证了本题解自己按 2 亿日活
算出的 3.2TB inbox 缓存量级是否处在合理区间；本题解与原文的分歧在于：原文没有给出"剔除
头部账号能带来多少写放大下降"的量化数字，本题解把这个下降算成了具体的 8.9 倍。
