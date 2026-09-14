---
id: cc-performance-budget-bounds-multiply
node: performance.budget
type: qa
---
## Q
A spec says "up to 10^5 requests" in one paragraph and "up to 10^5 targets" in another. Your router picks the least-loaded target by scanning all targets. Both bounds look small. Why does the performance test fail?

## A
**Bounds stated in different sentences multiply.** A scan per request is O(R × T) = 10^10, not 10^5.

- Write the product down the moment you see a second limit; that product, not either bound, is the size of your problem.
- Fix: make the hot query sub-linear. A min-heap of `(load, index)` gives the least-loaded target in O(log T) per request.
- The rule generalises: any per-event loop over all entities is quadratic even when each bound alone is comfortable. See [[cc-performance-hot-loop-rescan-entities]].

## Q zh
题面在一段里说「至多 10^5 个请求」，在另一段说「至多 10^5 个目标」。你的路由靠扫描所有目标来挑负载最轻的那个。两个上界看起来都不大。为什么性能测试会挂？

## A zh
**写在不同句子里的上界是要相乘的。** 每个请求扫一遍就是 O(R × T) = 10^10，不是 10^5。

- 看到第二个上限的那一刻就把乘积写下来；问题的规模是这个乘积，不是其中任何一个。
- 修法：把热点查询做成次线性。一个 `(load, index)` 的最小堆让「最轻负载」变成每请求 O(log T)。
- 规律可推广：任何「每个事件遍历所有实体」的循环都是平方级的，哪怕单看每个上界都很舒服。见 [[cc-performance-hot-loop-rescan-entities]]。
