---
nodes: [problems.components.rate-limiter]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/011-rate-limiter
tags: [no-archive]
---
# jkaus324/machine-coding-interview-questions — API Rate Limiter

值得读：同一道题的五语言对照（C++／Java／Python／Go／JS）外加一份 `DESIGN.md` 答案导读，
适合看"同一个设计换一种语言会长成什么样"。它把套餐分级（`UserTier` FREE／PRO／ENTERPRISE）
当成一等公民，按套餐下发不同限额，这一点比本题解讲得细，值得借鉴到"工厂按 key 查套餐再造状态"
那条追问上。分歧在于它的骨架是 Java／C++ 味的继承体系：接口上有 `allowRequest()` 和
`getRequestCount()` 这样的 getter，还要配一个 `RateLimiterFactory` 来选算法；
Python 里一个工厂函数（甚至一个 lambda）就够了，`@property` 取代 getter。
并发部分它止步于"加一把全局锁"，也没有讨论按 key 的状态怎么回收——而这两点正是本题解第 3 关的重心。
仓库无 LICENSE 文件，故只链接不摘录。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/011-rate-limiter)
%% trellis:end %%
