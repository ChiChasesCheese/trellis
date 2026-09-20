---
nodes: [problems.foundations.rate-limiter]
url: https://blog.cloudflare.com/counting-things-a-lot-of-different-things/
---
# Counting things: A lot of a different things

值得读：Cloudflare 工程博客一手给出了滑动窗口计数器近似公式的完整推导，以及在 4 亿次
真实请求、27 万个来源上测得的准确度数字——误判率 0.003%，估计速率与真实速率平均相差约
6%——是"近似限流算法在生产规模上够用"最直接的证据。本题解沿用了同一个滑动窗口计数器
公式处理 sustained 层，但额外把令牌桶分给了 burst 层单独处理，原文只讨论单一限流场景，
没有区分两种时间尺度的配额。
