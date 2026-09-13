# q41 Observability Metrics — report

## 摘要
本题是**重建题（非真题）**。已知线索只有 `catalog/discovery/2026-09/C_batchA.md` `## C1` 记录的
一件事——interviewdb.io 上存在一道裸标题「Observability」的 Stripe OA 题（Coding，2026-08 被发现
更新），正文区域全程是前端占位符（"Loading practice workspace…" / "No questions are available
yet"），多次 WebFetch 均拿不到规则、输入输出格式、函数签名或样例。旁证是 PracHub 上一道 onsite
系统设计题《Design a Count-Metrics Monitoring Platform》，主题（指标/计数/监控平台）高度相关，
但它是系统设计题而非编码题，且正文本身也没抓到，`C_batchA.md` 原文明确写"只能当主题旁证，不能当
题面"。因此本题的规则、输入输出格式、4 个 part 怎么切——**全部是本仓库自拟**，只保留"可观测性"这个
主题方向（指标事件流 → 时间窗聚合 → 告警规则）。

## Sources & confidence
**置信度：极低**——见上，除了标题和大致领域方向，没有任何规则文本可依据。来源见 `problem.md`
底部 "Sources" 一节（`catalog/discovery/2026-09/C_batchA.md` `## C1`、interviewdb.io 标题确认、
PracHub 系统设计题作为主题旁证）。

## 各 part 设计思路
1. **Part 1**：解析 `timestamp,metric_name,labels,value` 事件行，按 `(metric_name, 规范化
   labels)` 分组聚合 `count/sum/avg`。核心是行式解析纪律——4 种独立的"畸形行"原因（字段数不对、
   timestamp 不是非负整数、value 不是合法浮点、labels 既不是 `-` 也不是合法 `key=value;...`）
   都要被跳过并计数，而不是让程序崩溃；`labels` 还要做规范化（`b=2;a=1` 和 `a=1;b=2` 必须合并成
   同一个 series）。
2. **Part 2**：引入 `WINDOW <size> <step>`，把 Part 1 的裸聚合换成按时间窗分桶——`step == size`
   是不重叠的滚动（tumbling）窗口，`step < size` 是重叠的滑动（sliding）窗口，同一个事件在滑动
   模式下会落进多个窗口，这是设计好的行为而不是 bug。每个非空 `(metric,labels,window)` 组合再加
   两个百分位数（`p50`/`p90`，nearest-rank 定义，显式写出 `ceil` 公式避免不同候选人对"百分位"的
   理解分歧）。实现上用 `bisect` 在按时间排序好的每条 series 上做窗口范围查询，而不是对每个事件
   反推它属于哪些窗口——窗口数量通常远小于事件数量，这样效率更高也更好写。
3. **Part 3**：在 Part 2 的窗口统计之上叠加告警规则——每条规则独立维护一个 `OK/FIRING` 状态机，
   要求"连续 `trigger_n` 个窗口满足条件才触发，连续 `clear_n` 个窗口不满足才解除"（去抖/防抖动，
   现实告警系统的标准设计）。所有规则共享同一条"全局窗口时间线"（`0..max_k`，`max_k` 由整个事件
   流决定，不是某条规则自己的数据决定）——这样一条规则对应的指标"突然不上报了"也会被正确地当作
   一串 `count=0` 的窗口继续推进 `consecutive_false`，而不是被跳过。
4. **Part 4**：把 Part 3 的"离线批量计算"换成"按到达顺序处理事件流"，模拟真实流式系统的
   watermark 机制——每个事件有一个 `primary = timestamp // step` 主分桶；如果一个事件的主分桶
   落后于"已见过的最大主分桶 - 允许迟到窗口数 `L`"，就被丢弃并计入 `DROPPED`，否则正常并入它所属
   的（可能多个，滑动模式下）窗口。丢弃之后再跑一遍**和 Part 3 完全相同**的规则状态机。

## Tie-break / 确定性设计（S08）
- Part 1/2 用 `(metric_name, canonical_labels[, window])` 的字典序排序输出——Python 元组比较
  天然给出多级排序，不需要额外分支。
- Part 3/4 的告警转移行**不排序**，就用 `RULES` 小节里规则出现的原始顺序——因为每条规则自己的
  转移序列本来就是按窗口时间线天然递增的，强行排序反而会破坏"这是一条时间线"的语义；这个"不排序
  才是对的"决定本身就是 `S08` 要考的点（测试里专门验证了两条不同 label 的规则按 `RULES` 出现
  顺序而不是按 metric 名字母序输出）。

## Hidden tests 会考的坑
- Part 1：labels 顺序打乱后必须合并成同一 series；4 种畸形行原因都要能各自触发且互不影响计数。
- Part 2：偶数长度窗口的 `p50`（rank 落在中点靠后的那个元素，而不是取两者平均——这是本题自拟的
  nearest-rank 定义，不是插值定义，测试专门锁死这一点）；滑动窗口下一个事件出现在两个不同窗口
  里的重复计数。
- Part 3：`gt` vs `gte` 在恰好等于阈值时的分歧（`count==threshold` 下 `gt` 不触发、`gte` 触发）；
  `rate` 分母为 0 时被定义成 `0.0` 而不是崩溃或视为"未知"；一条规则的目标 metric 在整个输入里
  从未出现过，依然要沿着别的 metric 决定的 `max_k` 走一遍全 0 窗口序列。
- Part 4：`L=0` 时"同一个主分桶内的乱序到达"不算迟到（不能把"乱序"和"迟到"混为一谈，只有真正
  落后于 watermark 才丢）；专门构造了一个"丢弃与否直接改变某条 `ALERT_ON` 是否出现"的用例，
  确保候选人真的把丢弃的事件从聚合里剔除，而不是只在计数器上做样子。
- 格式：`MALFORMED`/`DROPPED` 两行永远存在（哪怕是 0），且顺序固定（`DROPPED` 在 `MALFORMED`
  之前）；所有聚合数值统一用 `.2f` 语义格式化，不做自定义四舍五入。

## Complexity & measured cost
Part 1：`O(n)`。Part 2：`O(n log n)`（按 series 排序一次）+ `O(windows × log n)`（每个窗口一次
二分查找）。Part 3：`O(rules × max_k × log n)`。Part 4：`O(n log n + rules × max_k × log n)`。
实测（`random.Random(0)` 生成 10 万条事件、20 个 metric、300s 窗口）：`solution.py` 直接调用
`part2`/`part3`/`part4` 均在 0.2–0.4 秒量级完成；`test_perf_1e5_events` 通过 `run_script` 子进程
测量，预算 2s / 256MB，实测远低于预算。

## 测试清单
25 个测试——part1: 5 · part2: 5 · part3: 5 · part4: 7；其中 edge: 15 · fmt: 1 · io: 3 ·
perf: 1（markers 按主 part marker 计数，edge/fmt/io/perf 可与 part marker 叠加）。

## 本题覆盖的知识点
- **S02**（行式解析）：Part 1 的 4 种独立畸形行判定（字段数、timestamp、value、labels）全部
  跳过并计数而非崩溃，加上 labels 字符串的规范化（排序 `key=value` 对）——解析之上还有一层
  "同一实体的不同字符串表示必须归一"的纪律。
- **S12**（时间与分桶）：`window k` 覆盖 `[k*step, k*step+size)` 的半开区间算术，`timestamp //
  step` 求主分桶，`max_k` 由全局最大 timestamp 推导——所有时间桶计算都是显式的整数除法/取模，
  没有隐式的浮点时间戳假设。
- **S05**（阈值语义）：`gt/gte/lt/lte` 四种比较符覆盖"严格 vs 非严格"，`count`（计数）与
  `rate`（比率，分母为 0 时显式定义为 0）覆盖"计数 vs 比率"的语义区分，两条测试专门锁死
  `count==threshold` 处的分歧。
- **S10**（事件流与状态翻转）：Part 3/4 的 `OK/FIRING` 状态机——只在真正发生翻转时才输出一行，
  连续触发/解除计数器独立维护，`trigger_n=1` 的"立即重新触发"边界被专门测试到。
- **S16**（滑动窗口）：`WINDOW <size> <step>` 里 `step < size` 时的重叠窗口成员关系，一个事件
  落进多个窗口是被测试直接断言的正确行为，而不是需要去重的 bug。
- **S08**（确定性排序）：Part 1/2 按 `(metric, labels[, window])` 多级排序；Part 3/4 刻意**不**
  排序、保留 `RULES` 输入顺序，两种"确定性"分别被测试锁定。
- **S09**（字节级输出格式）：所有聚合数值用 `.2f` 语义格式化并在 `problem.md` 里明确"匹配
  Python 的 `f'{x:.2f}'`，不要自造舍入规则"；`MALFORMED`/`DROPPED` 两个尾行永远存在（含值为 0
  时）且顺序固定。
