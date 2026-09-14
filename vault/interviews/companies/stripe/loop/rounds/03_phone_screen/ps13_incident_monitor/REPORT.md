# ps13 Incident Monitor — report

## Summary
按 `(merchant_id, status_code)` 分组的滚动窗口告警监控题。Part 1 的规则（闭区间滚动窗口求和、
`TRIGGER`/`RESOLVE` 严格镜像的阈值方向语义、不发连续同类型事件）**来自一份真实候选人报告**，
经 PracHub 结构化题面交叉印证（两个独立数值样例均验证通过）；但该报告标题与 catalog 记录的
「Incident Monitor」不同，无法确认是同一道题，且候选人自己说"二三部分有点忘了"。因此本题
**只有 Part 1 是"部分线索复原"，Part 2-4 的规则、全部输入输出格式、part 划分都是本仓库自拟**，
problem.md 顶部已加醒目警示块。四个 part 依次覆盖：单一全局规则（真实）→ 乱序到达（自拟）→
按商户覆写规则（自拟）→ 双阈值升降级状态机（自拟），刻意把 S04/S05/S10/S12/S16 五个技能点都用上。

## Sources & confidence
low-medium（Part 1）／本仓库自拟（Part 2-4，无独立 confidence 可言）。证据链：
1. PracHub `detect-trigger-and-resolve-events`（id 7608）页面内嵌候选人第一人称原始报告
   （`created_at: 2026-01-15`, `interview_round: "Technical Screen"`, `is_ai_assisted: false`），
   中文原文明确给出四字段 log、按 pair 分组、TRIGGER/RESOLVE 语义、"应该要用 queue"，但"二三部分
   有点忘了"。
2. 同页面 PracHub 结构化题面（同一份报告自动生成）给出完整规则公式（`[t-window_size+1, t]` 闭区间、
   `< threshold` ⇄ `>= threshold`）与两个数值样例；本 session 独立 `curl` 复抓（2026-09-03）核对与
   `catalog/discovery/2026-09/C_batchB.md` `## C9` 记录一致，且本 session **手动重新验证了两个数值
   样例的计算过程**（逐条 log 手算滚动窗口和，结果与页面给出的 Expected Output 完全吻合）。
3. **无法确认同一性**：PracHub 标题「Detect Trigger and Resolve Events」与 catalog 记录的
   「Incident Monitor」不同；`interviewdb.io` 全量翻页未命中"Incident Monitor"标题；GitHub
   `divyavenn/coding_problems` 148 文件名关键词检索 0 命中——两条均为"未找到"旁证，不是决定性证据。

按 catalog 惯例这属于"部分线索"（Part 1 规则大概率属实，但标题/part 划分不可考），故 problem.md
顶部加了警示块，Part 1 的 Confidence 定为 low-medium，不敢定 high。

## Approach by part
1. **Part 1**：按 `(merchant_id, status_code)` 建 `deque[(ts,count)]` + 累加和，逐条处理已排序的
   log；窗口滑出用 `while dq[0][0] < ts - window + 1: pop`；用一个 `triggered: bool` 每 pair 独立
   记录当前状态，只在状态真正翻转时才 append 事件——"不发连续同类型事件"是这个状态记录方式的自然
   推论，不需要额外去重逻辑。
2. **Part 2**：与 Part 1 规则完全相同；实现上 `part2 = part1`（`_parse_and_sort` 本来就会按
   `(timestamp, input_order)` 稳定排序，对已排序输入是幂等操作）——两个 part 分开纯粹是因为
   Part 1 的真实规则明确承诺输入已排序，Part 2 不做这个假设，不是代码逻辑不同。
3. **Part 3**：在 Part 1 引擎基础上加一个 `rule_for(merchant)` 回调，从"商户覆写表"里查，查不到
   落回默认规则；同一套 `_events_single_threshold` 引擎直接复用，只是每个 pair 用的 `(window,
   threshold)` 从常量换成了按 merchant 查表。
4. **Part 4**：把 Part 1 的"二状态（低于/高于阈值）"泛化成"三档（0/1/2）"，每次电平变化时按跨越的
   边界数量逐个发事件（`range(old+1, new+1)` 向上 / `range(old-1, new-1, -1)` 向下），天然支持
   "一步跨两档"的场景（发两条事件，同一个 timestamp）。

## Pitfalls hidden tests target
- **阈值方向镜像**：TRIGGER 是"从 `< threshold` 变为 `>= threshold`"，RESOLVE 是反方向——两个方向
  的严格/非严格恰好相反，`test_count_exactly_equal_to_threshold_triggers` 专门锁死"等于阈值算触发"
  这一侧。
- **pair 之间状态隔离**：`test_independent_pairs_do_not_share_state` 专门设计成"两个 pair 各自都
  不够阈值，但加在一起会够"——如果实现用了一个全局共享的 sum/deque 而不是按 key 分开，这个测试会
  假阳性触发。
- **tie-break 是输入顺序，不是 merchant_id 字典序**：`test_tie_broken_by_input_order_not_merchant_id`
  正反各测一次（交换两行输入，输出顺序也要跟着交换），防止"顺手按 merchant_id 排序"这种看似合理实则
  错误的实现。
- **Part 3 的规则是按商户固定的，不随时间变化**：`test_two_merchants_different_window_sizes_interleave_correctly`
  故意让两个商户的窗口大小差异悬殊（1 秒 vs 100 秒），验证合并后的时间序输出是真的按事件发生时刻
  排序，而不是按商户分组后各自输出。
- **Part 4 多级跳变**：一条 log 让某个 pair 从 0 档直接跳到 2 档（或反向），必须在同一个 timestamp
  上依次发出两条事件（`TRIGGER` 后 `ESCALATE`，或 `DEESCALATE` 后 `RESOLVE`），不能只发跳变后的
  终态事件、也不能只发第一个边界事件——这是本题设计里最容易漏掉的分支。
- **两个阈值边界都是非严格 `>=`**：`test_count_exactly_on_warn_and_crit_boundaries` 同时锁死 WARN
  和 CRIT 两侧的边界方向，防止只对其中一个边界写对。

## Complexity & measured cost
`_events_single_threshold` / `_events_two_level` 都是均摊 `O(n)`：每条 log 入队一次，每条历史 log
最多从其所属 pair 的 deque 里出队一次，`rule_for`/字典查找均为 `O(1)`。`_parse_and_sort` 的排序是
`O(n log n)`（Part 2 的乱序输入必须排序；Part 1/3/4 对已排序输入排序是等价于 `O(n log n)` 的"确认"
开销，可接受）。实测：`test_perf_200k_logs_out_of_order`（Part 2，20 万条乱序 log，100 个商户 ×
4 个 status_code = 400 个 pair）在预算 2s / 256MB 内完成（数字见测试运行结果）。

## Test inventory
29 tests — part1: 12 · part2: 5 · part3: 5 · part4: 7；edge: 13 · fmt: 2 · io: 4 · perf: 1。
（早期草稿里 part1 与 part4 各有一个函数都叫 `test_zero_log_lines`，Python 会让后定义的悄悄覆盖前一个
——flake8 F811 抓到了这个问题，修复后测试总数从 28 变为 29，是一次真实的"测试被吞"修复，不是凑数。）
（数字为 `pytest --collect-only -m <marker>` 实测计数。）

## 本题覆盖的知识点
- **S04**（按 key 分组聚合）：每个 `(merchant_id, status_code)` pair 独立维护 deque/running
  sum/state，绝不共享——专门配了 `test_independent_pairs_do_not_share_state` 直接测这个。
- **S05**（阈值语义，`<` vs `>=` 的方向性）：TRIGGER/RESOLVE 互为镜像，Part 4 把这个语义翻倍成两个
  独立边界（WARN/CRIT），是本题被刻意放大的核心考点。
- **S10**（事件流 + 状态翻转）：TRIGGER/RESOLVE 是最经典的两状态翻转模型；Part 4 把它泛化成三档
  状态机，且要求"一步跨两档"时按边界顺序逐个发事件，而不是只发终态。
- **S12**（时间分桶/滚动窗口的闭区间边界纪律）：`[t-window+1, t]` 闭区间，边界测试覆盖"恰好在窗口
  内"与"刚好滑出窗口"两侧。
- **S16**（滑动窗口/限流式计数器）：per-key `deque` 维护"仍在窗口内"的记录，滑动时從左侧逐个弹出
  过期记录，累计和随之增减——这是 rate-limit/token-bucket 类问题的标准实现范式。

## 与 q41 的区别
`problems/q41_observability_metrics`（OA 阶段，纯重建题，指标聚合 → 时间窗 → 告警规则）与本题
`ps13_incident_monitor`（电面阶段，Part 1 规则来自真实候选人报告 + 本仓库自拟扩展）主题相邻，
都属于"可观测性/监控告警"知识域（S24），但规则集是两回事，练习时不要混着背：
- **来源与置信度不在同一量级**：q41 是本仓库按 OA 阶段常见题型纯自拟重建的，没有候选人报告锚点；
  ps13 的 Part 1 有真实候选人报告 + PracHub 结构化题面双重印证（虽然标题对不上，按"部分线索"处理），
  Part 2-4 才是纯自拟——两题"重建程度"完全不同，不能互相当作对方的补充证据。
- **分组维度可能不同**：ps13 严格按 `(merchant_id, status_code)` 二元组分组；q41 是"指标聚合"，大概率
  按单一 metric 名或 metric+标签维度分组——不要假设两题分组 key 结构一样。
- **规则语义落点不同**：ps13 的核心是 TRIGGER/RESOLVE（以及 Part 4 的 ESCALATE/DEESCALATE）严格镜像
  的阈值方向语义 + 逐条 log 增量式重新评估状态；q41 是"指标聚合 → 时间窗 → 告警规则"更通用的三段管线，
  窗口聚合方式（sum/avg/max？）、告警规则形状（单阈值/多档/滞回？）都可能与 ps13 不同——**不要把 ps13
  这里 `[t-window_size+1, t]` 闭区间求和的具体公式当成 q41 的公式去套**。
- **事件命名不同**：ps13 用 `TRIGGER`/`RESOLVE`/`ESCALATE`/`DEESCALATE`；q41 的事件命名（如果有）应以
  q41 自己的 problem.md 为准，两套字符串不能混用。
- 本节写作时 `problems/q41_observability_metrics` 尚未在本仓库落地（据任务说明由另一位代理并行建设
  中），以上是基于任务描述做的预防性区分，并非逐条核对过 q41 最终题面——**q41 落地后应回来核对本节
  是否需要更新**，处理手法参照 `loop/rounds/06_coding_onsite/cd01_subscription_email_scheduler/
  problem.md` 里对 `q07_subscription_notifications` 的处理方式（同一手法：先声明"故意用不同字段/
  事件名/输出格式"，避免两题被当成同一套规则背诵）。

## Open points
- 未确认 PracHub 这道「Detect Trigger and Resolve Events」是否真的就是 catalog 记录的「Incident
  Monitor」——如果后续拿到更明确的标题匹配证据（或反证），应回来调整 problem.md 顶部警示块的措辞，
  甚至可能需要把置信度从 low-medium 上修或彻底改判为"标题孤证、规则未知"。
- Part 2-4 的具体输入输出格式（`PART n` 行式协议、`DEFAULT_WINDOW=... RULES=<k>` 的参数行设计、
  两档阈值的事件命名）是本仓库为覆盖技能点自拟的，与任何已知真实题面无关——如果后续拿到这道题
  （或任何同源题）Part 2/3 的真实转录，大概率需要整个重写而非小修。
