# int02 Payments reconciliation client — report

## Summary
一个最小可行的"我方账本 vs Stripe 侧记录"对账客户端：分页拉取全部 charge、用注入式 `sleep`/`rng` 让
429/5xx 重试逻辑可以在测试里瞬间跑完、发幂等退款、生成三类差异报告，外加从零手写一遍 webhook 签名验证
和事件去重。四个 part 里没有一行算法，全部是"生产可用的 HTTP 客户端该有的边界处理"——这正是 Simplify 转
述的校招 VO 原话（"handling pagination, rate limits, and idempotency"）和 Leon 指南列出的失败模式
（"只取分页第一页、无限重试无退避、支付流程静默失败"）指向的能力。

## Sources & confidence
Medium-high：三份独立来源（Simplify 校招 VO 转述、Leon 面试指南、programhelp 实习 VO 流程描述）各自提到
"分页/限流/幂等/webhook"里的若干项，互相印证这是 Integration 轮的常见主题范围，但**没有一份来源给出逐
part 拆分或原始 API 形状**——`loop/raw/github_repos.md` §3.2 明确写"Payment Reconciliation...均未找到公
开复刻 repo"。因此本题的 4-part 结构、`/v1/*` API 具体字段、`data/ledger.csv` 内容全部是本仓库原创设
计（基于 `docs.stripe.com` 官方文档的真实语义，不是编造），不是逐字题面还原，这点在 problem.md
Clarifications 里写明。

## Part-by-part approach
1. `fetch_all_charges`：`while True` 循环 + `starting_after` 游标，每页请求都走 `with_retry`；用
   `page["data"][-1]["id"]` 作为下一页游标，不用额外排序（服务端保证倒序时间）。
2. `with_retry`：唯一区分 429 与 5xx 的逻辑分支——429 读 `Retry-After` 直接睡那么久（服务端已经算好了），
   5xx 自己指数退避（`0.05 * 2**(attempt-1)` 起步）+ 抖动；非 429 的 4xx **不进重试分支**，立即重新抛出
   （`raise` 不带参数，保留原始 traceback）。`sleep`/`rng` 都是参数，测试传入纯记录型函数验证退避数值，
   全程 0 秒真实等待。
3. `refund`：把 `Idempotency-Key` 放进每次 HTTP 尝试的 header 里（而不是只在第一次尝试时加）——因为
   `with_retry` 可能真的重发这个 POST，key 必须在每次重发时都存在且相同。`reconcile` 用两个 dict + 三次
   集合运算（`-`/`&`）做 O(n+m) 对账，字段名映射（本地 `amount_cents` vs 远端 `amount`）在函数体里显式
   写清楚，避免面试时口头解释"为什么两边字段名不一样"却代码里悄悄用错字段。
4. `verify_webhook` 从零实现（不 import mockserver 的 `verify`），四步：拆 `t`/`v1` → 拼
   `signed_payload` → HMAC-SHA256 → `hmac.compare_digest` 常数时间比较 + 时间戳容忍度检查；任何格式错误
   都返回 `False` 而不是抛异常（防御性解析，和 int01 Part 3 的 PNG 魔数校验同一模式）。`handle_event` 用
   一个可变 `set` 做去重，按 `event.id` 而不是 `created`（`docs.stripe.com/webhooks` 原文明确警告不要用
   `created` 判断顺序或去重）。

## Pitfalls hidden tests target
- `fetch_all_charges` 只取第一页就返回（`has_more` 没检查）—— `test_fetch_all_charges_paginates_across_multiple_pages`
- 429 重试不看 `Retry-After`、固定睡一个写死的秒数 —— `test_with_retry_retries_429_using_retry_after_header`
  断言 `sleeps == [3.0]`（header 里写的是 3）
- 把所有 4xx 都当成"可重试的临时错误" —— `test_with_retry_does_not_retry_non_429_4xx` 断言 `calls["n"] == 1`
  （只调用一次，没有重试）
- 达到 `max_attempts` 后吞掉异常返回 `None`/空结果，而不是把最后一次错误抛给调用方 —— `test_with_retry_reraises_after_max_attempts`
- `refund` 重试时忘记透传 `Idempotency-Key`，导致同一逻辑操作产生两笔退款 —— 未显式构造网络中断场景（本
  地 mockserver 没有"随机丢响应但请求已处理"这种故障注入），改用直接的重放测试
  `test_refund_idempotent_replay_returns_same_id` 验证 key 语义本身
- `reconcile` 用错字段名（本地 `amount_cents` 当远端字段读，反之亦然）—— `test_worked_example_reconcile`
  用真实 mockserver 数据加两个精确构造的金额不一致案例
- `reconcile` 输出顺序依赖字典迭代顺序（Python 3.7+ 虽然保留插入序，但输入乱序时插入序不等于排序）——
  `test_reconcile_lists_are_sorted_by_charge_id`
- `verify_webhook` 用 `==` 而不是 `hmac.compare_digest` 比较签名（时序攻击面）—— 未直接测时序（需要统计
  实验，超出单元测试范畴），在 problem.md 追问 6 里作为口头考点
- `verify_webhook` 容忍度边界 `<=` vs `<` 搞反 —— `test_verify_webhook_within_tolerance_boundary`（300s
  仍有效，301s 失效）
- `handle_event` 第二次调用清空或覆盖 `store` 而不是追加 —— `test_handle_event_idempotent`

## Complexity + measured time/memory
`with_retry`/`fetch_all_charges`/`refund`：单次操作 O(1) 加常数次网络往返；分页整体 O(charge 总数 /
limit) 次请求。`reconcile`：两个 dict 构建 O(n+m)，三次集合运算 O(n+m)，无嵌套扫描。测得：10 万条本地 +
10 万条远端记录对账 < 0.2s（本机测量，预算 2s，见 `test_perf_reconcile_100k_rows`）。

## Test inventory
29 tests — part1: 6（2 happy + 2 edge + 2 io）· part2: 5（2 happy + 3 edge）· part3: 10（4 happy + 4 edge
+ 1 fmt + 1 io）· part4: 8（2 happy + 5 edge + 1 io）。
按 marker 统计：part1 6 · part2 5 · part3 10（含 1 fmt、1 io）· part4 8（含 1 io）· edge 13 · fmt 1 ·
io 4 · perf 1。
`rtk proxy python3 -m pytest loop/rounds/05_integration/int02_payments_reconciliation -q` → 29 passed；
`IMPL=starter` 同一命令 → 20 failed / 9 passed（`with_retry` 默认实现 `return fn()` 在 happy-path 无异
常时能通过、`reconcile` 空输入/无差异输入等边界默认返回值凑巧正确，其余全部按预期失败）。

## Skills exercised
S02 CSV 解析 · S11 幂等/去重（`Idempotency-Key` 重放 + webhook `event.id` 去重）· S16 限流/退避（429
Retry-After + 5xx 指数退避+抖动）· S18 错误路径分类（可重试 vs 不可重试状态码）· S19 增量设计
（`with_retry` 被两个 part 复用）· S24 领域知识（Stripe 分页/幂等/webhook 签名标准写法），对照
`skills_matrix.md`。

## 边写边说什么（onsite 话术）
- 打开 mockserver README 先复述分页语义给面试官确认："`starting_after` 传上一页最后一条的 id，循环到
  `has_more` 为 false——这是标准的游标分页，不是 offset，我直接按官方文档的写法来。"
- 写 `with_retry` 前先画一个小表格（429 vs 5xx vs 其他 4xx 分别怎么处理），口头过一遍再动手："429 服务端
  已经告诉我要等多久，我直接读 header；5xx 我自己估计，加抖动防止一堆客户端同时重试；别的 4xx 重试没有
  意义还可能有副作用，直接抛出去。"
- 实现 `refund` 时主动提醒自己（也讲给面试官听）："这个函数会被 `with_retry` 包一层，意味着同一个 POST
  可能真的发出去两次——我必须确保 `Idempotency-Key` 在每次尝试里都带上同一个值，不能在重试时漏掉或者换
  一个新 key。"
- `verify_webhook` 写完第一版后主动提"我现在用的是 `==` 比较，我要改成 `hmac.compare_digest`，因为逐字
  节比较存在时序侧信道"——即使面试官没问，先讲出来比等被问更能体现安全意识。
- 时间紧张时优先保证 Part 1-3（拉数据、重试、对账）逻辑正确、错误处理完整，Part 4 如果来不及写完整实现，
  先把 `verify_webhook` 的四个步骤讲清楚（哪一步防篡改、哪一步防重放、哪一步防时序攻击），比匆忙写一个
  有漏洞的实现更能拿到部分分。

## Review（2026-09-02）

**方法**：按 `loop/tasks/review_checklist.md` 逐条过一遍，实际跑 `rtk proxy python3 -m pytest`（solution
全绿 × 2 次、`IMPL=starter` 一次）、`python3 loop/mock.py serve int02 --port 0`（子进程方式验证能起停干
净）、手动用 `fetch_all_charges` + `load_ledger` + `reconcile` 对着真实 mockserver（`seed=7, n=20`）重放
worked example，逐字段核对与 problem.md 一致。

### F（必须修）—— 发现 0 个功能性 bug，2 个 lint 类 F 项
改动前逻辑本身已经正确（分页、429/Retry-After、5xx 指数退避+抖动、非 429 4xx 不重试、`max_attempts` 耗尽
抛出、`Idempotency-Key` 每次重试都带、`reconcile` 字段名映射与三路排序、`hmac.compare_digest` 常数时间比
较、`handle_event` 按 `event.id` 去重）都已正确实现且被对应测试覆盖，worked example 手动重放结果与
problem.md 完全一致，不需要改任何行为。真正踩到 F 线的只有 lint 层面：
1. `starter.py` / `starter_template.py` 预留的 `csv`/`hashlib`/`hmac` import（候选人实现 `load_ledger`/
   `verify_webhook` 才会用到）在候选人动手之前是未使用的，`flake8 --select F` 直接报 3 个 F401 ×2 文件 ——
   按 checklist "starter 预留 import 可加 `# noqa: F401`" 加了行内注释修复，两个文件保持逐字节一致。
2. `test_int02.py` 里 `test_perf_reconcile_100k_rows` 的两个列表推导式续行缩进不满足 flake8 E127（无关
   F 类，但影响 `loop/lint.sh` 整体通过）——跑 `loop/lint.sh --fix` 时被 black 一并规范化。
`loop/lint.sh loop/rounds/05_integration/int02_payments_reconciliation` 现在全绿（0 F 类、0 其他）。

### S（建议修，已做）
- **把 HTTP 调用收敛成一个独立函数**：改前 `_get_json`（GET）和 `refund._do`（POST）各自手写一份
  `urllib.request.Request(...) + urlopen(...)`，两份逻辑几乎重复。改为一个 `_request(base_url, method,
  path, api_key, body=None, extra_headers=None) -> dict`（14 行，`solution.py:74-88`），`fetch_all_charges`
  的分页循环、`refund`、`main()` 的 `PART 2` 分支现在都只调用它，不再各自碰 `urllib.request.Request`/
  `urlopen` 的细节。业务逻辑（分页判断 `has_more`、退款的幂等 header 拼装、`main` 的分发）和"怎么发一次
  HTTP 请求"彻底分层。
- `refund` 从"内嵌一个闭包 `_do()`"简化成直接把 `_request(...)` 包一层 lambda 传给 `with_retry`，函数体
  从 ~30 行降到 8 行，可读性更直接。
- 其余 S 项本来就已经做到位，未改动：`sleep`/`rng` 全程可注入、`with_retry` 单一职责 ≤ 35 行、类型标注、
  一句话 docstring 打头、错误处理用具体异常类型（`urllib.error.HTTPError`，无裸 `except:`）、`reconcile`
  用两个 dict + 集合运算 O(n+m) 不是嵌套扫描、`fetch_all_charges`/`refund` 复用同一个 `with_retry`。

### 测试新增
补了 1 个：`test_with_retry_does_not_retry_timeout_or_connection_errors`（part2/edge）—— 直接单测
`with_retry` 面对 `TimeoutError`（`URLError` 的子类，代表连接超时/失败）时不重试、立即抛出、`fn()` 只被
调用一次，覆盖 checklist 里"429/5xx/超时/连接失败/幂等冲突/签名验证失败"六类网络错误路径中原先只用
`fetch_all_charges` 间接测过的"超时"一类，且是纯单元测试（不依赖真实网络/真实超时，不引入 flaky 风险）。
其余五类（429、5xx、连接失败、幂等冲突、签名验证失败×5 种畸形/边界）改前就已覆盖，未新增。

测试数：29 → **30**（part1 6 · part2 6（含新增的 timeout 边界）· part3 10 · part4 8，edge 14 · fmt 1 ·
io 4 · perf 1）。

### 回归结果
- `rtk proxy python3 -m pytest loop/rounds/05_integration/int02_payments_reconciliation --tb=short`：
  **30 passed**，连跑 2 次结果一致（无 flaky，fixture 每个测试独立起停 mockserver，`server.shutdown()` +
  `server.server_close()` 保证端口/线程不残留）。
- `IMPL=starter` 同一条命令：**20 failed / 10 passed**（比改前的 9 passed 多 1 个——新增的 timeout 测试直
  接调 `with_retry`，starter 的占位实现 `return fn()` 对这个用例碰巧也是"立即抛出、只调用一次"的正确行
  为，属于 checklist 允许的"边界默认值凑巧正确"，不是测试空洞；其余 20 个失败照旧覆盖每个真正需要实现的
  行为点）。
- `python3 loop/mock.py serve int02 --port 0`：子进程方式验证首行输出 `listening on http://127.0.0.1:...`
  后 `SIGTERM` 能正常退出（`returncode -15`），无残留进程。

### 遗留问题
无。四个 part 的行为、排序、错误路径、幂等语义与 problem.md 逐条核对一致；未发现需要进一步修的 F/S 项。

### mockserver bug
未发现。核对了 `loop/mockserver/payments.py` 的分页游标语义、`Idempotency-Key` 缓存/冲突逻辑、
`_read_json_or_form` 的 `Content-Type` 判定、`sign`/`verify` 的签名格式，均与 `problem.md`/
`loop/mockserver/README.md` 描述一致，与 `solution.py` 的假设吻合（未改动 `loop/mockserver/`）。
