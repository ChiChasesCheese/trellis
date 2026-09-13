# cd04 · Rate Limiter（四部分）— 基础、内存、边界坑、线程

**类型：** 现场编程练习（onsite Programming Exercise） · **阶段：** 虚拟现场"Programming Exercise"（60 分钟，4 部分） · **最近一次出现：** 2026-09-01（1point3acres 题库，仅有目录，抓取）
**出现频率：** 1 次独立提及且带有具体的四部分目录（1point3acres 题库 "Rate Limiter"：Part 1 The Basics → Part 2 Saving Memory → Part 3 Tricky Situations → Part 4 Handling Multiple Threads）；与同仓库的 `problems/q23_rate_limiter/problem.md`（一道*不同*的、来源更充分的 OA 限流题，8 次独立提及）交叉核对以获得贴近现实的数字与边界约定 · **置信度：** 低-中——四部分*结构*（基础 → 内存 → 边界 → 并发）直接来自一份抓取的目录（只能读到小节标题，读不到正文）；本 problem.md 中的每一个数值示例、内存分析要求、具体的"tricky situations"清单，以及线程安全约定，都是**重构**出来的，目的是与该目录以及 q23 已确立的约定（窗口边界、"被拒绝的请求不计入记录"）保持内部一致。这是一道刻意与 q23 不同的练习：q23 是滑动窗口 / per-client / 加权 / 令牌桶（OA 风格，"每部分加一个新特性"）；这道题则是"把同一个简单限流器做成生产可用级别"（同样是 OA 风格，但四个部分是基础 → 内存 → 边界情况 → 并发，而不是新算法）——不要照搬 q23 的解法，两题的部分划分和类结构都不同。

## 背景
每一个 Stripe API key 都受限流保护。根据 1point3acres 目录，这道题的现场版本并不要求你每部分都
发明一种新算法（那是 q23 的路数）——它要求你拿一个*最简单*的正确限流器，一步步推向可以真正上线
部署的水平：先让它正确，再让它不泄漏内存，再处理朴素实现会出错的边界情况，最后让它在真实并发流量
下也安全。这条推进路线——"基础 → 内存 → 边界情况 → 线程"——是本轮里事务级别题和账户调度器题里
也出现过的、Stripe 现场面试的常见模板。

## 类接口
```python
class RateLimiter:
    def __init__(self, limit: int, window_s: int) -> None
    def allow(self, client_id: str, t: int) -> bool
    def evict_idle(self, now: int) -> int
    def log_size(self, client_id: str) -> int      # observability hook, see below
```
`log_size(client_id)` 返回当前**在内存中**为该 client 保留的时间戳数量（未知/从未出现过/已被驱逐
的 client 返回 0）——它存在的唯一目的是让 Part 2 的内存上界声明（每个活跃 client 为 `O(limit)`）
能在测试里被直接断言，而不是只能从行为里推断；它是唯一一个存在理由纯粹是可测试性、而非生产契约的
方法；如果面试官问"这个方法为什么存在"，应当把这一点说出来。
`limit` 是每个 client 每个窗口内允许通过的最大请求数。`window_s` 是以**秒**为单位的窗口长度；内部
所有计算和比较都转换为**毫秒**（`window_ms = window_s * 1000`），因为每次调用传入的时间戳参数 `t`
是整数**毫秒**时间戳——这里特意把这一点钉死，因为"`t` 到底是秒还是毫秒"是本仓库见过的所有限流器
写法里最常见的隐藏 bug 来源；本题明确采用毫秒，并在每个方法的 docstring 里都注明这一点。

## 规则
### Part 1 — 基础：正确的滑动窗口日志
为每个 client 维护一份所有**被放行**请求的时间戳日志。`allow(client_id, t)` 当且仅当该 client
日志中落在**左开右闭窗口 `(t - window_ms, t]`** 内的条目数 `< limit` 时返回 `True`（与
`problems/q23_rate_limiter` 相同的边界约定，保持仓库内一致性）——即 `count + 1 <= limit` 时放行。
被拒绝的请求**绝不添加进日志**（一连串拒绝本身不应计入限额，也不应延长任何人的锁定期）。第一版
实现可以把见过的每个时间戳都存进一个无界 `list`，并在每次调用时重新扫描——这样做是正确的，但
**内存无界、每次调用 O(n)**；这正是 Part 2 要解决的问题。

### Part 2 — 节省内存：有界日志 + 空闲 client 驱逐
Part 1 的草案中存在两处独立的内存泄漏，都必须解决：
1. **单个 client 的日志无限增长。** 把原始 list 换成 `collections.deque`，并在每次调用时先从
   **左侧** pop 掉过期条目（`<= t - window_ms`），再计数/追加。由于被拒绝的请求永不追加，一个
   client 的 deque 永远不会超过 `limit` 个条目——每个*活跃* client 的内存是 `O(limit)`，而不是
   `O(该 client 历史上发起过的全部请求数)`。
2. **死 client 的累积。** 一个只发起过一次请求、之后再也没回来的 client，其条目会永远留在外层
   `dict` 里。新增 `evict_idle(now: int) -> int`：对每个 client，按 `allow` 同样的方式对其 deque
   按 `now` 裁剪；如果裁剪后 deque **变空**（即该 client 在 `(now - window_ms, now]` 内没有任何
   请求），就把该 client 从所有内部状态中彻底移除。返回被驱逐的 client 数量。周期性地调用
   `evict_idle`（例如每个窗口一次）能把总内存上界限制在 `O(limit × A)`，其中 `A` 是尾随窗口内的
   活跃 client 数——而不是 `O(limit × 历史上连接过的所有 client 数)`。

### Part 3 — 边界坑（明确钉死，而不是留作"未定义行为"）
- **时钟回拨。** 如果某个 `client_id` 的 `t` 小于该 client**历史上传入过的**最大 `t`（无论放行还是
  拒绝），该调用**不会被拒绝**——而是在做任何其他事情之前先**向前钳制**到该 client 最后一次见到的
  `t`（窗口检查、日志裁剪、日志追加都使用钳制后的值）。面试时的理由：对时钟回拨抛 `ValueError`
  会让限流器本身，在每次 NTP 让两台采集器出现时钟偏差时，都变成一次生产事故的源头；钳制则优雅
  降级为"当作现在到达处理"。这同时也保持了每个 client 内部 deque 的单调不减性，而这正是 Part 2
  裁剪逻辑所依赖的假设。
- **`limit == 0`。** 对所有 `client_id`、永远、无条件拒绝。不抛 `ValueError`——把限流器配置为零
  容量是一种合法（虽然没用）的配置，例如运维人员想彻底切断某个异常 key 的全部流量。
- **大量同时请求（多次调用 `t` 相同）。** 用普通规则即可处理：窗口 `(t - window_ms, t]` 本身包含
  `t`，因此同一 `t` 上的 `k` 次调用，恰好 `min(k, 剩余容量)` 次被放行，按**调用顺序**评估——平局
  不需要特殊处理，它们本就是 Part 1 规则的自然结果。
- **`client_id == ""`。** 空字符串是和其他任何值一样合法的字典 key；它代表"匿名 client"，拥有
  自己独立的额度。类层面无需特殊处理——这一点直接针对 `RateLimiter.allow` 测试，而不是通过
  `main()` 的 `ALLOW` 命令，因为该流式格式按空白分割 token，无法把一个空 token 与"完全没有该字段"
  区分开（`"ALLOW  100".split()` 会悄悄坍缩成两个 token）；这是面向行的 `main()` 协议本身的
  局限，不是类的问题。
- **极大的 `t`**（例如 `10**15`，相当于一个合理的远未来毫秒时间戳，或者真正巨大的合成值）。
  Python 整数不会溢出；一门朴素定长计数器的语言需要显式检查这一点，即便 Python 绕开了这个问题，
  这一点也值得在面试中口头指出。

### Part 4 — 多线程
`allow` 和 `evict_idle` 必须能在多个线程针对**同一个** `RateLimiter` 实例并发调用时保持安全，且
`allow` 必须保持**精确**（不是最终一致，也不是近似）——如果一个窗口内合法允许 `limit` 个请求，
并发调用者累计必须恰好看到 `limit` 个 `True`，绝不能更多（竞态会导致容量被重复占用），在有足够
并发尝试的前提下也绝不能更少。参考实现把 `allow` 和 `evict_idle` 的整个临界区（读日志、裁剪、
计数、决策、追加）都包在一把贯穿实例生命周期的 `threading.Lock` 里——关于 per-client 锁替代方案
以及为什么在本题规模下不值得为此增加复杂度的讨论，见 REPORT.md。

## 演示样例
```
RateLimiter(limit=3, window_s=1)     # window_ms = 1000
allow("u", 0)    -> True    (log: [0])
allow("u", 100)  -> True    (log: [0, 100])
allow("u", 200)  -> True    (log: [0, 100, 200]; count was 2 < 3)
allow("u", 300)  -> False   (window (-700, 300] holds 0,100,200 -> count 3, not < 3; log unchanged)
allow("u", 1000) -> True    (window (0, 1000]; the entry at t=0 is now excluded (left-open) ->
                              count 2 < 3; log: [100, 200, 1000])
```
```
RateLimiter(limit=2, window_s=60)                 # window_ms = 60000
evict_idle(now=0)              -> 0               # no clients yet
allow("a", 0)                  -> True
allow("b", 0)                  -> True
evict_idle(now=59999)          -> 0                # both still in window (0, 59999]
evict_idle(now=60000)          -> 2                # window is now (0, 60000]; entry at t=0 is EXCLUDED
                                                     # (left-open) -> both deques empty -> both evicted
allow("a", 60000)              -> True              # "a" was evicted, comes back with a fresh budget
```
```
RateLimiter(limit=1, window_s=1)          # window_ms = 1000
allow("c", 500)  -> True     (log: [500])
allow("c", 300)  -> False    (t=300 < last-seen 500 -> clamped to 500; window (-500, 500] already
                               holds the entry at 500 -> count 1 == limit -> DENIED; log unchanged)
allow("c", 1500) -> True     (real time now advances past the clamp; window (500, 1500] excludes
                               the entry at t=500 (left-open) -> count 0 < 1 -> True; log: [1500])
```

## 隐藏测试已知会瞄准的边界情况
- 窗口边界：排除 `t - window_ms`，包含 `t`（精确对应 q23 的约定）
- 被拒绝的请求不得追加进日志（一连串拒绝不应延长任何人的有效锁定期，也不应"过期"，因为它本来就
  没被记录）
- Part 2：在大量拒绝调用与放行调用交替之后，一个 client 的 deque 永不超过 `limit` 个条目——直接
  检查内部状态大小来断言这一点，而不只是从行为推断
- Part 2：`evict_idle` 恰好移除截至 `now` 窗口为空的那些 client（边界 `==` 会驱逐，早一毫秒不会），
  并返回精确的驱逐数量；一个之后又回来的被驱逐 client 拿到全新、满额的额度（旧历史被清空，不是
  "被记住"）
- Part 3：小于某 client 最后一次见到的 `t` 的值会被钳制，而不是被拒绝，且钳制是**按 client** 隔离
  的（client A 的时钟回拨不影响 client B 的时钟）
- Part 3：`limit == 0` 立即拒绝每一次调用，不抛异常
- Part 3：多次在同一 `t` 上调用——恰好 `limit` 次成功，按确定性调用顺序
- Part 3：`client_id == ""` 表现得和其他任何 client 一样，拥有独立额度
- Part 3：`t` 达到 `10**15` 量级不会崩溃或出现异常行为
- Part 4：8 个线程 × 每线程 1000 次并发 `allow()` 调用，针对同一个共享 client / 同一个共享窗口，
  必须**恰好**产生 `limit` 个 `True`——不是"大约"，也不是"通常"——用精确相等断言，证明临界区在
  竞争下真正是原子的
- 跨多个 client 的 10 万次顺序 `allow()` 调用必须在预算内舒适地跑完

## 现实世界中见过的变体
- 来源目录中"Saving Memory"这一节，与许多限流器写法中常见的通用模式一致（不是 Stripe 特有的）：
  用朴素的全量历史日志对比经过裁剪的滑动窗口日志；一种被接受但**本题未实现**的替代方案（放入
  follow-up）是*近似*滑动窗口：`上一窗口计数 × 重叠比例 + 当前窗口计数`，用牺牲精确性换取每个
  client O(1) 的内存（完全不需要按请求记日志）——如果被问"如何进一步节省内存"，可以提这个权衡。
- `problems/q23_rate_limiter` 是本仓库的另一道限流题：滑动窗口（全局 → per-client → 加权）加上
  令牌桶，有自己的 `SlidingWindow`/`RateLimiter`/`TokenBucket` 类和一个 `CLEANUP` 流命令。那道题
  "清理空闲 key 的内存"这个 follow-up，与本题 Part 2 的 `evict_idle` 是同一个想法，独立得到印证——
  交叉引用即可，不要合并；两题的类结构和部分划分是刻意不同的（本题没有 per-client 权重、没有令牌
  桶，并且把线程安全独立设为一个部分，而不是 follow-up 讨论）。

## 本题测试的能力
技能：S03 建模（每个 client 的状态）· S05 严格与非严格窗口边界 ·
S12 时间窗口 · S16 滑动窗口日志 · S17 内存上界分析（陈述并证明 `O(limit × A)` 上界，而不只是
写代码）· S18 校验/优雅降级策略（钳制 vs 抛异常）· S19 增量式设计 · S21 标准库熟练度
（`collections.deque`、`threading.Lock`）· A15 并发下的线程安全（精确而非近似的正确性）

## 来源
- 一亩三分地题库 "Rate Limiter" TOC（`loop/raw/cn_forums.md` 第 ~108 行）："题目是'设计并实现一个能
  跟踪 API 访问模式、强制请求限流的 rate limiter'，文章按 4 个 part 递进：Part 1 The Basics → Part 2
  Saving Memory → Part 3 Tricky Situations → Part 4 Handling Multiple Threads" — 只有目录，正文
  在登录墙后面；本 problem.md 中的每个数值示例和规则都是与该目录保持一致的重构，不是原始出处的
  数字。
- `loop/raw/en_forums.md` §6.2（C8，现场编程环节中提到的限流器）——用于交叉核对本题所遵循的
  "45-60 分钟、2-4 个部分、每部分递增复杂度"现场面试模板。
- `problems/q23_rate_limiter/problem.md` ——本仓库来源更充分的滑动窗口/令牌桶限流题；此处仅用于
  窗口边界约定（左开右闭）和"被拒绝的请求不计入记录"这条规则，两题保持一致以确保统一性，**不用于**
  其部分划分或类结构，本题刻意不照搬这些。

## 面试官会怎么追问
1. "Part 1 的实现每次 `allow` 都要重新扫一遍这个 client 的全部历史吗?复杂度是多少?" — 逼你先说出
   朴素版本是 `O(n)` 每次调用、且内存无上界,而不是一上来就写"优化版"蒙混过关;这正是 Part 2 存在
   的理由,面试官想看你能不能自己说出这个动机,而不是背答案。
2. "你说 `evict_idle` 把内存上界从'历史上出现过的所有 client'降到'当前活跃的 client',那这个上界的
   数学表达式是什么?" — 期望候选人现场写出 `O(limit × A)`(`A` = 活跃 client 数),并解释为什么
   `evict_idle` 必须被**定期调用**才有意义——它自己不是被动触发的。
3. "时钟回拨你选择 clamp 而不是抛异常,如果反过来 Stripe 要求'必须拒绝任何回拨的请求',你的实现要
   改哪几行?对 `deque` 的'单调递增'假设有什么影响?" — 检验候选人是否真的理解 clamp 存在的原因
   (维护 deque 单调性),而不是随手选了一个分支。
4. "`limit=0` 为什么不抛异常,而 Part 1 的 `window_s` 或者 `limit` 为负数呢?" — 一个开放追问,期望
   候选人现场做出并说明一个新的、内部一致的选择(比如构造时校验 `limit < 0` / `window_s <= 0` 抛
   `ValueError`,因为那是配置错误而非运行时正常状态,而 `limit == 0` 是合法配置),而不是照搬 `==0`
   的处理方式去处理负数。
5. "Part 4 你用一把全局锁包住整个 `allow`,如果 QPS 极高、client 数量巨大,锁竞争会不会成为瓶颈?
   怎么优化成 per-client 锁?" — 期望候选人提出"每个 client 一把锁 + 一把额外的锁保护外层 dict 的
   创建/删除(或者用 `defaultdict` + 只读升级为写锁的双重检查)",并能说清楚这比全局锁复杂在哪、
   何时才值得付出这个复杂度。
6. "为什么 8 线程 × 1000 次并发的测试断言的是'恰好等于 limit',而不是'大约等于 limit'?这在验证
   什么?" — 检验候选人是否理解"exact"这个词在并发正确性测试里的分量——它在证明临界区真的是原子
   的,而不是"大部分时候没有明显的竞态"这种弱得多的保证。
7. "如果这是分布式部署,多个进程/机器共享同一个 rate limit 预算,你的内存内 `deque` + `Lock` 方案
   还成立吗?要改成什么?" — 期望候选人提到 Redis + Lua 脚本(或等价的原子操作)做跨进程的滑动窗口
   计数,并能指出'进程内锁'和'分布式协调'是两个完全不同量级的问题。
