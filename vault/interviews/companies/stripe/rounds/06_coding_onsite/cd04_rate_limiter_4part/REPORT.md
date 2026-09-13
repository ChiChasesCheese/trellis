# cd04 RateLimiter（四部分）— 报告

## 摘要
一个单一的滑动窗口日志限流器，贯穿 Stripe 常见的现场面试模板——基础 → 内存优化 → 边界情况 →
并发——而不是本仓库另一道限流题（`problems/q23_rate_limiter`）"每部分新增一种算法"的形态。真正
有意思的内容几乎全在 Part 2-4：证明（而不仅仅是声称）每个 client 的内存上界为 `O(limit)`，为朴素
规格说明留下的每一种"未定义行为"挑选并证成一个确定性答案，以及让整套实现在并发访问下做到"完全
正确"，而不只是"大概率没事"。

## 来源与置信度
低-中——四部分结构（Basics / Saving Memory / Tricky Situations / Multiple Threads）直接来自一份
抓取的一亩三分地目录（`loop/raw/cn_forums.md` 第 ~108 行）；该页面正文在登录墙后面，因此所有数值
演示样例、内存分析要求的具体措辞、"tricky situations"的具体清单，以及 problem.md 中整套线程安全
约定，都是在与该目录、以及 `problems/q23_rate_limiter` 已有来源的窗口边界约定保持内部一致的前提下
重构出来的。应把这道题视为"形状对、数字是编的"，而非逐字转录。

## 分部分思路
1. **Basics**：每个 client 维护一个已放行时间戳的 `deque`；`allow` 统计落在
   `(t - window_ms, t]`（左开右闭，与 q23 一致）区间内的条目数，若 `count < limit` 则追加 `t`；
   被拒绝的调用永不追加。一份实现同时覆盖了这部分和 Part 2——problem.md 中作为 Part 1 起点描述的
   "朴素无界 list"只是一种叙事手法（用来说明为什么需要 Part 2），不是需要维护的第二条代码路径。
2. **Saving memory**：deque 在*每次*调用计数之前都会从左侧裁剪，因此永远不会超过 `limit` 个条目
   （被拒绝的请求永不追加，所以是"裁剪 + 只在放行时追加"的组合共同保证了这个上界——不是单靠裁剪
   本身）。`evict_idle(now)` 关闭了第二处内存泄漏（外层 `dict` 里永久滞留的死 client）：对每个
   client 的 deque 按 `now` 裁剪，并把裁剪后变空的 client 直接丢弃。额外加了
   `log_size(client_id)`，纯粹作为可测试性钩子，让"每个活跃 client 是 `O(limit)`"这个断言可以被
   直接验证，而不是靠计时去推断。
3. **Tricky situations**：五种行为各钉死为一个确定性答案——时钟回拨对每个 client *钳制*（而非
   拒绝），钳制正是维持 deque 单调递增假设、使 Part 2 裁剪逻辑成立的关键；`limit == 0` 无条件拒绝且
   不抛异常（这是一个合法、只是没用的配置）；同一时间戳的突发请求不需要特殊处理（Part 1 的规则
   本身就能按调用顺序正确处理）；`client_id == ""` 就是另一个普通的 dict key；极大的 `t` 在
   Python 中不是问题（任意精度整数），但值得口头指出这一点是语言相关的。
4. **Threads**：整个 `allow`/`evict_idle` 的临界区（钳制 → 裁剪 → 计数 → 决策 →
   追加/驱逐）都包在一把 `threading.Lock` 里，因此 8 个线程各自对同一个 client 打 1000 次调用，
   累计恰好看到 `limit` 个 `True`——用精确相等断言证明，而不是模糊的"差不多对"检查。曾考虑过
   per-client 锁的方案，但为这道练习题否决了：它需要*第二把*锁来保护外层 `dict`，让 client 的
   创建本身不出现竞争（两个线程第一次为同一个全新 client 调用都命中 `setdefault` 本身就是一种
   竞态），这是实打实的额外复杂度，只有在实测到单一全局锁的锁竞争确实成为瓶颈时才值得——值得作为
   一个现场追问提出来，但不值得在这个规模下不请自来地实现。

## 隐藏测试瞄准的坑
- 窗口边界恰好排除 `t - window_ms`、包含 `t`，与 q23 保持一致，确保仓库内两道限流题口径统一
- 一连串拒绝本身绝不能延长任何锁定期（没有记录任何东西，就没有东西可以过期，也不会抬高下一个
  窗口的计数）
- 即便对 `limit=5` 的限流器打 200 次调用，`log_size` 也不会超过 `limit`——这是 Part 2 承诺的内存
  上界的直接、与实现无关的证明
- `evict_idle` 的边界（`==` 窗口边缘会驱逐，早一毫秒不会）；被驱逐的 client 回来后拿到的是真正
  全新的额度，而不是记住的耗尽额度
- 时钟回拨钳制是按 client 隔离的——一个 client 的回拨不能泄漏到另一个 client 的时钟
- `limit == 0` 永不抛异常，永远拒绝，包括对空字符串 client 也一样
- 相同时间戳的突发请求恰好解析为 `min(k, 剩余容量)` 个放行，按调用顺序
- `client_id == ""` 只在类层面测试——`main()` 按空白分割的命令格式无法把一个空 token 与"没有
  token"区分开，这被记录为协议层面的局限，不是类本身的 bug
- `t` 达到 `10**15` 量级时行为与小 `t` 完全一致（Python 整数不会溢出）
- 对同一个 client 并发 8×1000 次 `allow()` 调用恰好产生 `limit` 次成功——证明这把锁真正串行化了
  临界区，而不只是降低了竞态发生的频率

## 复杂度与实测开销
`allow`/`evict_idle` 每次调用均摊 `O(1)`，唯一例外是 `evict_idle` 对当前所有被跟踪 client 的一次
线性遍历（每个时间戳最多被 push 和 pop 各一次）。内存：每个活跃 client 为 `O(limit)`，总量为
`O(limit × A)`，其中 `A` 是尾随窗口内的活跃 client 数（直接通过 `log_size` 证明，而非仅靠论证）。
性能测试：通过 `run_script` 对 2,000 个 client 顺序执行 10 万次 `allow()` 调用——远低于 2s / 256MB
的预算。

## 测试清单
21 个测试——part1: 4 · part2: 4 · part3: 10（含 2 个 io、1 个 perf、1 个 fmt）· part4: 3（含一个
精确计数并发断言、一个 per-client 独立性并发断言、一个 allow+evict_idle 并发压力测试）；
edge 12 · fmt 1 · io 2 · perf 1。

## 涉及的技能
S03 建模（每个 client 的状态）· S05 严格/非严格窗口边界 · S12 时间窗口 ·
S16 滑动窗口日志 · S17 内存上界分析（有证明，不只是声称）· S18
校验/优雅降级策略（钳制 vs 抛异常）· S19 增量式设计 · S21 标准库熟练度
（`collections.deque`、`threading.Lock`）· A15 并发下的线程安全（精确而非近似的正确性）

## 复盘（2026-09-02）
按 `loop/tasks/review_checklist.md` 逐条复核，结论：solution.py 本身在上一轮已经写得很干净，本轮只是
补齐两处遗漏，没有发现结构性问题。

**改了什么**
- `solution.py`：`allow()` 方法之前没有 docstring（`_effective_t`/`evict_idle`/`log_size` 都有，唯独
  这个核心方法没有），补了一句话 docstring 说明窗口规则和"拒绝不入账"的行为，对齐 S 项"docstring
  一句话说清做什么"以及题面里反复强调的窗口口径。
- `starter.py` / `starter_template.py`：`loop/lint.sh --fix` 后 flake8 报两个 F401（`threading`、
  `collections.deque` 未使用——这是 TODO stub 有意预留的 import，供候选人实现时用），按 checklist
  允许的方式加 `# noqa: F401` 消除，两个文件内容保持逐字一致（diff 确认 identical）。
- 其余 diff（`test_cd04.py` 里大量的空白改动）是 `loop/lint.sh --fix` 做的 black 110 列重排（注释前
  多余空格被压成两个空格），没有改动任何断言或逻辑。

**为什么**
- 这题的 4-part 结构（basics → memory → tricky edges → threads）本身已经把"未定义行为"逐条钉死、把
  内存上界用 `log_size` 直接可断言、把并发正确性用"恰好等于 limit"而不是模糊断言验证，是这批题里
  review 负担最小的一个；改动集中在文档完整性和 lint 合规，没有修复任何行为 bug。

**验证**
- solution 侧：`rtk proxy python3 -m pytest <dir> --tb=short` 连续跑 4 次（含专门为并发测试重复的 3
  次），21/21 全绿，无 flaky。
- starter 侧：`IMPL=starter rtk proxy python3 -m pytest <dir> --tb=no`，20 failed / 1 passed（唯一
  通过的是空输入测试，starter 的 `run_commands` TODO 桩本就返回 `[]`，与空输入的期望输出巧合一致，
  不是空洞测试）。
- 三个 worked examples 用 `solution.py` 直接跑了一遍，输出与 problem.md 逐字一致。
- `loop/lint.sh loop/rounds/06_coding_onsite/cd04_rate_limiter_4part` 通过（0 exit code）。

**遗留**
- 无功能性遗留项。REPORT.md 里已经讨论过的 per-client-lock 优化、分布式限流等，按原文档定位仍然是
  "面试追问话术"而非本题范围内要实现的东西，不在本轮改动范围内。
