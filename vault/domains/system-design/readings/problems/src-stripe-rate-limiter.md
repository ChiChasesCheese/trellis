---
nodes: [problems.foundations.rate-limiter]
url: https://stripe.com/blog/rate-limiters
---
# Scaling your API with rate limiters

值得读：Stripe 工程博客一手披露了生产环境真实跑的四层限流/丢弃防御——令牌桶实现的
request-rate limiter、concurrent-requests limiter、为关键操作预留机器的 fleet-usage
load shedder、以及最后一道防线 worker-utilization load shedder，并给出了"限流代码本身
的 bug 或 Redis 故障都不该影响请求"这条 fail-open 原则和各层真实的月度拒绝量级。本题解
在此基础上补充了"为什么保护公平性的层可以 fail-open、保护后端自身的层反而要保守退化"
这条因果论证，原文没有展开这一层区别。

%% trellis:begin %%
## Source
[Open the original ↗](https://stripe.com/blog/rate-limiters)

## Archived copy
![[stripe-rate-limiters-clip]]
%% trellis:end %%
