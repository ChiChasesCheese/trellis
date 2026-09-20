---
nodes: [problems.components.rate-limiter]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/rate-limiter
---
# abhaypaswan/lld-python — Design a Rate Limiter

值得读：Python 实现，四种算法（固定窗口／令牌桶／滑动窗口日志／滑动窗口计数）齐全，
README 用一行 ASCII 输出把**边界突发**演示得极直观——同一段流量，固定窗口放行 10/10，
其余三种放行 5/10；它也明确说了 `now` 作为参数传入而不是算法自己读时钟，以及令牌桶必须惰性补充。
和本题解的分歧有三处：它让每个算法各自实现完整的 `allow(now, cost)`，于是"额度够不够、
还剩多少、cost 超上限怎么办、被拒不扣额度"这几条规则被抄了四遍，本题解把它们收进基类的
`check`，子类只答 `_used`／`_retry_after`／`commit`；它的状态回收是 `forget_idle(older_than)`，
正确性依赖调用方传对阈值，本题解改用"状态与新建等价即可丢"的 `is_idle` 不变量；
它没有锁，也没有"同时按用户和按接口"的两阶段组合判定。
