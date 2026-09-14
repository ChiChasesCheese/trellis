# int02 · Payments reconciliation client — 分页拉取 → 429/5xx 退避重试 → 幂等退款 + 对账 → webhook 验签
<!-- mockserver: payments -->

**Type:** onsite Integration（真实 HTTP 调用，非算法题） · **Stage:** 60 min，4 part · **Last asked:** 2026 校招 VO（Simplify 转述）
**Frequency:** Simplify 转述校招 VO 原话"transaction reconciliation script handling pagination, rate limits, and idempotency"；Leon 面试指南把 pagination / idempotency key / 429+Retry-After 退避 / 响应防御性解析列为 Integration 轮"四大边界情况"；programhelp 描述的实习 Integration 流程包含"调用外部 Payment API 获取交易数据 → 处理 webhook 回调 → 实现交易状态同步" · **Confidence:** medium-high for 主题范围（对账 + 分页 + 限流退避 + 幂等 + webhook，多份来源独立提到其中若干项，无一处给出完整逐 part 拆解或原题数据）；具体 part 切分、API 形状、`ledger.csv` 内容均为本仓库设计，不是逐字题面还原（英文侧综述明确指出"没有找到这道题的原始素材"，见 Sources）。

## Context
Stripe 内部有大量"我方系统记录 vs Stripe 侧记录"的对账场景（商户后台余额 vs charges API、本地发货记录 vs
payout API 等）。这道题模拟一个最小可行的对账客户端：连接一个 Stripe 风格的 payments API（本仓库
`loop/mockserver/payments.py` 复刻），把远端全部 charge 拉下来、和本地 CSV 账本比较，找出"本地缺记录 /
远端缺记录 / 金额对不上"三类差异；同时要正确处理真实 HTTP 客户端在生产环境必须处理的三件事：游标分页、
限流退避、幂等重试——外加一段 webhook 签名验证与去重逻辑。**不考算法**，考察对分布式系统边界情况（网络会
失败、请求会重复、事件会乱序）的直觉和 `docs.stripe.com` 这类真实文档的阅读能力。

## API 文档（`loop/mockserver/payments.py` 复刻的 Stripe 风格 payments API）
```
所有 /v1/* 请求需要 Authorization: Bearer sk_test_... ，缺失/格式错误 -> 401 authentication_error
所有响应带 Request-Id: req_<hex> header

GET /v1/charges?limit=&starting_after=&ending_before=
  游标分页（不是 offset 分页）：limit 默认 10，范围 1-100；starting_after/ending_before 二选一，
  互斥同传 -> 400。响应固定结构：
    {"object": "list", "url": "/v1/charges", "has_more": bool, "data": [...]}
  charge 字段：id, object, amount(整数分), currency, status(succeeded/failed/refunded),
  created(unix 秒), customer, metadata。按 created 降序（最新的在前）。
  非法 cursor / limit 越界 / 两个 cursor 同传 -> 400 invalid_request_error

GET /v1/charges/{id}
  200 单个 charge，或 404 {"error":{"type":"invalid_request_error","code":"resource_missing"}}

POST /v1/refunds   body: {charge, amount?}（amount 缺省 = 该 charge 未退款余额）
  可选 Idempotency-Key header：同 key + 同 body 原样重放上次响应（同一个 refund id）；
  同 key + 不同 body -> 400 idempotency_error。不带 key -> 每次都是新退款。
  已全额退款的 charge 再退 -> 400 charge_already_refunded；超过未退款余额 -> 400 amount_too_large

POST /v1/webhook_endpoints/test   body: {"url": "..."}
  服务端构造一个 charge.refunded 事件，用 HMAC-SHA256 签名（Stripe-Signature: t=<unix>,v1=<hex>，
  密钥 whsec_test_secret），POST 到给定 url，返回 {"delivered": bool, "response_status", "event"}

任意 /v1/* 超过限流 -> 429 {"error":{"type":"rate_limit_error",...}} + Retry-After: 1
```
（完整细节见 `loop/mockserver/README.md`。）

## Rules
### Part 1 — 游标分页拉取全部 charge
`fetch_all_charges(base_url, api_key, limit=100, sleep=time.sleep) -> list[dict]`：循环 `GET
/v1/charges?limit={limit}&starting_after={上一页最后一条的 id}`，直到某一页 `has_more` 为 `false`，
把所有页的 `data` 拼接成一个列表返回（保持服务端给的倒序时间顺序，不用重新排序）。每一页请求都通过
Part 2 的 `with_retry` 发出（透传 `sleep` 参数）。`Authorization: Bearer {api_key}` header。

### Part 2 — 429 / 5xx 重试退避（供 Part 1、Part 3 复用）
`with_retry(fn, max_attempts=5, sleep=time.sleep, rng=random.random)`：`fn` 是一个无参可调用对象，
执行一次 HTTP 尝试，非 2xx 时抛 `urllib.error.HTTPError`（`e.code` 是状态码，`e.headers` 是响应
header）。
- **429**：读 `Retry-After` header（秒，缺失/非法则按 1 秒处理），`sleep(retry_after)` 后重试——**不做
  指数增长**，服务端已经明确告诉你要等多久。
- **5xx**：指数退避 + 抖动：`base = 0.05 * 2**(attempt-1)` 秒，实际睡眠 `base + rng() * base`
  （`rng()` 返回 `[0, 1)`，所以最多睡到 2 倍 base）。
- **其他状态码（4xx 非 429）**：不重试，立刻把异常抛给调用方。
- 达到 `max_attempts` 次尝试后仍失败，把最后一次异常原样抛出。
`sleep`/`rng` 必须是可注入参数（默认 `time.sleep`/`random.random`），测试会传入假的记录型函数，**绝不
真的等待**。

### Part 3 — 幂等退款 + 对账
`refund(base_url, api_key, charge_id, amount, idempotency_key, sleep=time.sleep) -> dict`：`POST
/v1/refunds`，带上 `Idempotency-Key` header（**每次重试都要带同一个 key**——重试时如果漏发 key，服务端
会当成一次全新请求，产生第二笔退款）。通过 `with_retry` 发送。

`load_ledger(path: str) -> list[dict]`：读本地账本 CSV（表头 `charge_id,amount_cents,status`），返回
`[{"charge_id": str, "amount_cents": int, "status": str}, ...]`。

`reconcile(local_rows, remote_charges) -> dict`：比较本地账本与远端 charge 列表，返回
```python
{
  "missing_local":   [charge_id, ...],   # 远端有、本地账本没有的 id（按 charge_id 升序）
  "missing_remote":  [charge_id, ...],   # 本地账本有、远端没有的 id（按 charge_id 升序）
  "amount_mismatch": [{"charge_id", "local_amount_cents", "remote_amount_cents"}, ...],  # 按 charge_id 升序
}
```
三个列表都要按 `charge_id` 升序排列（确定性输出）；`amount_mismatch` 只统计两边都有记录、金额不一致的
情况（`local_amount_cents != remote_amount`，远端字段名是 `amount`，本地字段名是 `amount_cents`——注意
两边字段名不同）。

### Part 4 — Webhook 签名验证 + 幂等事件处理
`verify_webhook(payload: bytes, sig_header: str, secret: str, now: int, tolerance: int = 300) -> bool`：
**自己实现**（不 import `loop.mockserver.payments.verify`，即使它做的是同一件事——这道题就是要练手写
一遍）。`sig_header` 形如 `"t=<unix>,v1=<hex>[,v1=<hex>...]"`（可能有多个 `v1`，只要有一个匹配就算通
过）；步骤：拆出 `t` 和所有 `v1`；`signed_payload = f"{t}.".encode() + payload`；用 `secret` 对
`signed_payload` 算 HMAC-SHA256 十六进制摘要；**用 `hmac.compare_digest` 做常数时间比较**；`t` 与
`now` 差值超过 `tolerance` 秒（默认 300，即 5 分钟）视为过期，返回 `False`；`t`/`v1` 缺失或 `t` 不是
合法整数也返回 `False`（不抛异常）。

`handle_event(event: dict, store: set) -> bool`：`store` 是一个记录已处理过的 `event["id"]` 的集合
（原地修改，调用方在多次调用之间复用同一个 `store`）。第一次见到这个 `event["id"]` 返回 `True` 并把它
加入 `store`；重复投递（`store` 里已经有这个 id）返回 `False`，不重复处理。**按 `event.id` 去重，不要
用 `created` 时间戳**——`docs.stripe.com/webhooks` 明确说事件投递顺序不保证，且同一事件可能被投递多次。

### `main()` / `PART n` 驱动（供 io 测试）
第一行 `PART n`，后续每行是该 part 的参数：
```
PART 1
<server_url>
<api_key>                    输出: "{n} charges"

PART 2
<server_url>
<api_key>                    输出: "{page 条数} charges has_more={bool}"（对第一页做 with_retry 包装）

PART 3
<server_url>
<api_key>
<ledger_csv_path>            输出 3 行：
                              "missing_local: id1,id2,..."
                              "missing_remote: id1,id2,..."
                              "amount_mismatch: id(local=X,remote=Y),..."

PART 4
<secret>
<now>                         unix 秒整数
<sig_header>
<payload_json>                单行 JSON 字符串（不含换行）
                               输出: "True" 或 "False"
```

## Worked examples
`data/ledger.csv` 是针对 `loop.mockserver.payments.serve(seed=7, n=20)` 生成的确定性 charge 数据集手工
构造的对账场景（生成方式见文末"数据生成方式"）：18 条与远端一致（其中 2 条金额故意改错），本地额外多出
2 条远端不存在的记录，远端有 2 条本地账本没有收录。`reconcile(load_ledger("data/ledger.csv"),
fetch_all_charges(server, api_key))` 的结果：
```python
{
  "missing_local": ["ch_bz8wtp1dk7gj2at9kl4istbo", "ch_j1rumyt24d6nxpl38ep128rc"],
  "missing_remote": ["ch_local_only_1", "ch_local_only_2"],
  "amount_mismatch": [
    {"charge_id": "ch_89ti8lmanrshsajdobakivt1", "local_amount_cents": 1400, "remote_amount_cents": 1449},
    {"charge_id": "ch_9pdvdut8wchnw8vrer9rlf00", "local_amount_cents": 16800, "remote_amount_cents": 16817},
  ],
}
```
`with_retry` 的退避行为（`rng` 固定返回 `0.0` 便于举例，真实运行会加抖动）：
```
fn() 第 1 次抛 HTTPError(500) -> sleep(0.05 * 2**0 + 0) = sleep(0.05)
fn() 第 2 次抛 HTTPError(500) -> sleep(0.05 * 2**1 + 0) = sleep(0.10)
fn() 第 3 次成功 -> 返回结果，总共调用 fn() 3 次，sleep() 2 次
```
`verify_webhook` 用 mockserver 自带的 `sign()` 构造一个合法 header 验证往返：
```python
payload = b'{"id":"evt_1","type":"charge.refunded"}'
header = payments.sign(payload, "whsec_test_secret", t=1735689600)
verify_webhook(payload, header, "whsec_test_secret", now=1735689600)        # True（t 就是 now）
verify_webhook(payload, header, "whsec_test_secret", now=1735689900)        # True（差 300s，边界内）
verify_webhook(payload, header, "whsec_test_secret", now=1735689901)        # False（差 301s，超出容忍度）
verify_webhook(payload, header, "whsec_wrong_secret", now=1735689600)       # False（密钥不对）
```

## Edge cases hidden tests are known to target
- `fetch_all_charges` 必须真正翻页到 `has_more=false` 为止，只取第一页是最常见的偷懒实现
- 429 重试要读 `Retry-After` header 的秒数，不是自己瞎猜一个固定值或者不重试直接失败
- 5xx 重试是指数退避，不是每次固定睡眠相同时长
- 4xx（非 429，比如 400/401/404）**不应该**被当成"网络抖动"重试——重试一个必然失败的请求是纯粹浪费时
  间还可能造成副作用（比如重复扣费），这是"哪些错误可重试"这条边界的核心考点
- 达到 `max_attempts` 后必须把异常抛给调用方，不能吞掉错误静默返回空结果
- 连接被拒绝（`URLError`/`OSError`，不是 `HTTPError`）不应该被 `with_retry` 当成 HTTP 状态码错误处理
  （这里的设计选择是：网络层错误不重试，立刻抛出——面试官常会追问这个取舍）
- `refund` 的重试路径必须带上同一个 `Idempotency-Key`，否则一次超时后的自动重试会在服务端产生第二笔退款
- `reconcile` 的两边字段名不同（本地 `amount_cents`，远端 `amount`），直接比较错误字段名是常见 bug
- `reconcile` 三个输出列表都要排序，测试用乱序输入验证输出顺序稳定
- `reconcile([], [])` 返回三个空列表，不是 `None`/抛异常
- `verify_webhook`：篡改 payload、错误密钥、过期时间戳、缺 `t`/`v1` 字段的畸形 header，都必须返回
  `False` 而不是抛异常
- `verify_webhook` 的容忍度边界：`|now - t| == tolerance` 仍然有效（`<=`），`== tolerance + 1` 失效
- `handle_event` 同一个 `event.id` 第二次调用必须返回 `False` 且不能把 `store` 清空或覆盖已有条目
- `handle_event` 不同 `event.id` 都应该各自被处理一次（`store` 是按 id 去重，不是"只处理第一个事件"）

## Variants seen in the wild
- Simplify 转述的原话只说"handling pagination, rate limits, and idempotency"，没有提到 webhook；本仓库
  把 webhook 签名验证并入 Part 4，因为这是 Leon 指南和官方文档反复强调的"Bug squash 与 Integration 共同
  重灾区"，且和幂等去重（Part 3 的 `Idempotency-Key`、Part 4 的 `event.id` 去重）是同一类工程能力，放在
  一起考察更完整。
- programhelp 描述的实习版本要求"实现交易状态同步"而非纯只读对账；本版本的 `reconcile` 是只读比较（不
  写回任何一方），更贴近"生成对账报告"而不是"双向同步覆盖"，是对源材料的收窄。
- Leon 指南提到的"malformed response 防御解析"在本题体现为 `verify_webhook` 对畸形 header 一律返回
  `False` 而不是抛异常（防御性解析的通用模式，与 int01 Part 3 的 PNG 魔数校验同源）。

## What this tests
skills: S02 CSV 解析 · S11 幂等/去重（`Idempotency-Key` 重放 + webhook `event.id` 去重）· S16
限流/退避计数器（429 Retry-After + 5xx 指数退避+抖动）· S18 错误路径分类（哪些状态码可重试、哪些不可）·
S19 增量设计（`with_retry` 被 Part 1、Part 3 复用）· S24 领域知识（Stripe 分页/幂等/webhook 签名的标准
写法，对照 `docs.stripe.com`）

## 面试官追问（不少于 6 个）
1. "如果 `fetch_all_charges` 中途某一页失败到 `max_attempts` 耗尽，已经拉到的前几页数据怎么办？" ——
   期待：讨论是整体失败重来（当前实现的行为：异常直接抛出，调用方决定是否丢弃部分结果）还是支持"从上次
   失败的 `starting_after` 继续"的断点续传，并说明当前简化实现的取舍。
2. "429 和 5xx 的重试策略为什么不一样？" —— 期待：429 服务端明确给了 `Retry-After`，照做即可；5xx 是服
   务端没说清楚要等多久，客户端自己估计一个退避时间，还要加抖动防止大量客户端同时重试造成"雷鸣群"效应。
3. "`refund` 重试时如果第一次请求其实已经成功创建了退款，只是响应在网络中丢失了怎么办？" —— 期待：这正
   是 `Idempotency-Key` 存在的意义——服务端保存了第一次请求的响应，重试会原样重放而不是创建第二笔退款；
   连 500 错误响应本身也会被幂等重放（这是 `docs.stripe.com/api/idempotent_requests` 里容易被忽略的细
   节）。
4. "`reconcile` 对 100 万条记录要跑多快？当前实现是什么复杂度？" —— 期待：当前是两个 dict 构建 + 集合
   运算，O(n+m)，不是嵌套循环 O(n×m)；能讲清楚为什么用 dict/set 而不是对每条本地记录线性扫描远端列表。
5. "如果同一个 charge_id 在本地账本里出现了两次（重复行）呢？" —— 期待：当前 `load_ledger`/`reconcile`
   用 dict 会让后出现的行覆盖前面的，讨论这是否是期望行为，还是应该在 `load_ledger` 阶段就报错/去重。
6. "`verify_webhook` 为什么要用 `hmac.compare_digest` 而不是 `==`？" —— 期待：防时序攻击（timing
   attack）——`==` 逐字节比较会在第一个不匹配字节就提前返回，攻击者可以通过测量响应时间逐字节猜出正确签
   名；`compare_digest` 是常数时间比较。
7. "`handle_event` 的 `store` 如果是个内存里的 `set`，服务重启后会怎样？" —— 期待：识别这是简化实现，生
   产环境需要把已处理事件 id 持久化（数据库/Redis），否则重启后所有历史事件都会被当成"没处理过"重放一次。
8. "限流 429 的重试如果永远不成功（服务端限流永远没恢复）呢？" —— 期待：`max_attempts` 兜底会最终抛出异
   常，讨论调用方应该怎么处理彻底失败（告警、降级、人工介入），而不是无限重试。

## Sources
- Simplify（校招 VO 转述，2026）："transaction reconciliation script handling pagination, rate limits,
  and idempotency"（`loop/raw/en_forums.md` §5.3）
- Leon 面试指南（`https://leonstaff.com/blogs/stripe-technical-interview-bug-squash-integration-guide/`）：
  "评分点：文档使用、边界覆盖、API ergonomics、production-readiness；失败模式：假设 REST 约定不读文档、
  只取分页第一页、无限重试无退避、支付流程静默失败"
- programhelp.net《Stripe 2026 Summer Intern VO full interview process》：Integration 轮"调用外部
  Payment API 获取交易数据 → 处理 webhook 回调 → 实现交易状态同步"（`loop/raw/cn_forums.md`）
- `docs.stripe.com/api/idempotent_requests`、`docs.stripe.com/api/pagination`、`docs.stripe.com/webhooks`、
  `docs.stripe.com/rate-limits` 官方文档摘录（`loop/raw/stripe_official_and_api.md` §3.1/3.3/3.4/3.5）
- `loop/raw/github_repos.md` §3.2："Payment Reconciliation（支付对账，对接清算服务 API）...均未找到公开
  复刻 repo"——确认本题没有可参照的原始题面，本仓库是按上述来源的主题描述原创设计
- `loop/mockserver/README.md` §payments.py（本仓库对 payments API 的复刻实现，作为本题的 mockserver）

## Clarifications（本仓库自定，非题面原文）
- 没有任何来源给出这道题的逐 part 拆分或原始 API 形状；本仓库把"分页/限流/幂等"三个来源反复提到的能力点
  拆成 Part 1/2/3，webhook 验签作为 Part 4（理由见 Variants）——这是本仓库的结构化设计，不是还原。
- `data/ledger.csv` 不是任何真实数据，是针对固定 `(seed=7, n=20)` 的 mockserver 输出手工构造的对账场景
  （生成方式：先用 `random.Random(7)` 调用 `loop.mockserver.payments._generate_charges` 生成 20 条
  charge，取其中 18 条原样写入账本、故意改错 2 条的 `amount_cents`、跳过 2 条不写入、再额外手写 2 条远端
  不存在的 `charge_id`——总计 20 行，对应 worked examples 里的三类差异各自的数量）。`_generate_charges`
  的 `id`/`amount`/`status`/`currency` 字段只依赖 `random.Random(seed)` 的调用顺序，与调用时的墙钟时间无
  关（只有 `created` 字段是"当前时间 - 若干随机秒数"，因此本仓库不依赖 `created` 的具体值），所以
  `payments.serve(seed=7, n=20)` 在任何时候起服务，产出的这 20 条 charge 的 id/amount/status 都与
  `data/ledger.csv` 里编码的完全一致，可重复。
- `with_retry` 的具体退避公式（`0.05 * 2**(attempt-1)` 秒起步）是本仓库选择的具体数值，源材料只说"指数退
  避 + 抖动"，没有给出基准时长。
