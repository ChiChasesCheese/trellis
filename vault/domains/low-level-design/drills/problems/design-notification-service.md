---
nodes: [problems.components.notification-service, patterns.strategy, patterns.observer]
tags: [problem]
---
# Drill：通知服务（Notification Service）

一个**进程内**的通知服务：业务系统调一次"通知这个用户这件事"，系统按用户偏好把它扇出到邮件、
短信、推送。规模是几万用户、每秒几百条通知，渠道是会超时会拒收的外部网关。这道题看起来是
"写四个 `send_xxx` 方法"，四个渠道的差异却是全题最不重要的部分——**真正的考点是重试、限流、
去重、优先级这些逻辑写在哪**。照真实机考的节奏分关来做，做完一关再看下一关。时钟一律注入，
代码里不许出现 `datetime.now()`，测试里不许有一个 `sleep` 参与断言。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 12 分钟）：三个渠道躲在同一个协议后面；一次通知寻址到一个**用户**而不是一个地址；
  按偏好扇出；每个渠道都可能失败，**一个渠道失败不许影响另一个**；每次投递返回一个说得清
  "成功了还是为什么没成功"的结果对象——不许只返回布尔值。
- 第 2 关（约 12 分钟）：用户可以关掉某个渠道、给某个渠道设最低重要性门槛、设置静默时段
  （本地时间，**可以跨午夜**，按用户时区）；按"用户 × 渠道"的频次上限；以及一条优先级车道。
  **把"优先级"在排队上的具体含义说出来**：严格优先级会不会饿死低优先级？你怎么办？只说
  "我用了优先队列"是不及格的答案。另外答准一条：验证码撞上静默时段怎么办。
- 第 3 关（约 12 分钟）：失败分两类——瞬时（超时）按指数退避重试，永久（地址非法）一次都不重试；
  重试用尽进死信。**退避不许用 `time.sleep`**，用一个按到期时间排序的延迟堆加注入的时钟。
  再加幂等：键由调用方提供，粒度是"一次请求 × 一个渠道"，并写一个测试证明第二次提交
  **真的没有**调用渠道。最后写一个八线程加栅栏同时提交同一个 id 的用例。
- 第 4 关（选做）：加一个站内信或 webhook 渠道，以及给短信加一个专属短模板。判分点只有一个：
  这两件事是不是都只需要"注册一条数据"，派发器、偏好、限流器一行都不用改。

**怎么练**：把 `vault/domains/low-level-design/problems/notification-service/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/notification-service -q`。

**评分点**
- 可靠性写在派发器里一份，渠道只剩名字和 `send`；说得出装饰器栈为什么放不下跨渠道的限额与优先级（[[problems-notification-service-reliability-belongs-to-dispatcher]]）。
- 渠道是开放字符串加注册表而不是 `Enum`，并说得出"用类型安全换扩展性"这个代价（[[problems-notification-service-channel-is-not-an-enum]]、[[patterns-strategy-callable]]）。
- 优先级落实成分道 FIFO 加连续服务配额，答得出"低优先级会不会饿死"（[[problems-notification-service-priority-lanes-and-quota]]）。
- 幂等键由调用方提供，粒度是请求 × 渠道，去重表有 TTL 和清理（[[problems-notification-service-idempotency-key-and-scope]]）。
- `claim` 是一次加锁内的检查加占坑，说得出"先查后写"在单线程里永远测不出来（[[problems-notification-service-claim-is-check-then-act]]、[[concurrency-check-then-act]]）。
- 失败分瞬时与永久两类，用异常类型承载；结果状态不合成一句"失败"（[[problems-notification-service-transient-vs-permanent]]）。
- 退避靠延迟堆加注入时钟，堆里的元组带一个递增序号做平局裁决（[[problems-notification-service-backoff-uses-a-delay-heap]]）。
- 静默时段跨午夜的判断写对，且 URGENT 穿透；说得出"抑制还是延后"的取舍（[[problems-notification-service-quiet-hours-and-urgent]]）。
- 偏好、限额、模板全在**入队前**判完，重试路径不再重复计入限额（[[problems-notification-service-policies-before-the-queue]]）。
- 调用渠道时不持有任何锁；`dead_letters`、`history` 返回快照元组且有上限（[[problems-notification-service-never-call-provider-under-lock]]、[[oop-getter-collection-leak]]）。
- 限流器窗口空掉的 key 会被删掉，去重表有 TTL——通知服务里任何只涨不落的字典都是一次事故。

**题解**：[[solution-notification-service]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
