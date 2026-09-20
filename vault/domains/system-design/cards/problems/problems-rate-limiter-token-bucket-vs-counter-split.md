---
id: problems-rate-limiter-token-bucket-vs-counter-split
node: problems.foundations.rate-limiter
type: qa
step: 5
tags: [grown]
---
## Q
In a rate limiter that must enforce both a burst limit and a sustained limit for the same API key, why does the design use a token bucket for the burst tier and a sliding window counter for the sustained tier, rather than the same algorithm for both?

## A
A token bucket's defining property is that unused capacity accumulates as saved tokens that can be spent all at once, which is exactly what a burst limit needs to express: 'allow a short spike now, as long as the long-run average refill rate stays capped.' A sliding window counter has no such saved allowance — it estimates a smoothed rate from the current and previous window's counts and deliberately does not let extra capacity bank up, which matches what a sustained limit needs: a precise long-run average with no accumulated slack. Using the counter for burst would wrongly permit sustained overuse smoothed across windows, and using the token bucket for the sustained tier would let saved-up tokens from quiet periods produce longer-than-intended bursts later.

## Q zh
在一个速率限制器里，同一个 API key 既要有 burst 限制又要有 sustained 限制，为什么 burst 层用令牌桶、sustained 层用滑动窗口计数器，而不是两层用同一个算法？

## A zh
令牌桶的核心特性是：没花掉的容量会作为积攒的令牌保留下来，可以一次性花完——这正是 burst 限制需要表达的语义：'允许现在有一次短暂的突发，只要长期平均的补充速率仍被限制住'。滑动窗口计数器没有这种可积攒的余量——它用当前窗口和上一窗口的计数估算一个平滑速率，刻意不允许多余容量累积，这正好匹配 sustained 限制需要的语义：精确的长期平均值、不带累积余量。如果 burst 层用计数器，会错误地允许持续超量在多个窗口间被平滑掉；如果 sustained 层用令牌桶，安静期积攒的令牌会在之后产生比预期更长的突发。
