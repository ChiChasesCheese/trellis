# REVIEW_KEY · cr01 alert fan-out

> 先自己评审再看。优先级口径：**影响面 × 可能性 × 可发现性**（不易被测试/监控发现的静默故障优先级更高）。
> 位置行号对应 `starter/`（PR 合入后的状态）。`diff 内` 表示改动在 `pr.diff` 里；`diff 外` 表示问题在既有代码里，PR 只是"用了它"。

## 问题表（13 条：P0 4 · P1 5 · P2 4）

| ID | 位置 | 级 | 一句话问题 | 为什么是这个级别 | 修法 | 验收测试 |
|---|---|---|---|---|---|---|
| CR-01 | `worker.py:52` | P0 | 收到消息就 `delete`，之后才发送（diff 内） | 影响面：所有告警；可能性：每次部署/OOM/节点回收都会触发；可发现性极低——消息已删，没有任何痕迹。丢的是安全告警，业务后果最重 | 处理成功后再 `delete`；失败则不删，靠 visibility timeout 重投；崩溃安全 | `test_cr01_message_is_still_in_queue_while_it_is_being_sent`、`test_cr01_crash_mid_send_does_not_lose_the_alert` |
| CR-02 | `models.py:39`（diff 外），被 `worker.py:88` 使用 | P0 | 去重 key = `rule:alert_id`，不含 `tenant_id`；alert_id 只在租户内唯一 | 影响面：多租户产品里一个租户的告警会让另一个租户**永远收不到**同 id 的告警（静默吞通知）；可能性：自增 id 在两个租户间必然碰撞；可发现性低。PR 里看不出来，必须点开 `dedup_key` 的定义 | key 加 `tenant_id`；再加渠道（见 CR-05）：`tenant:rule:alert:kind:target` | `test_cr02_same_alert_id_in_two_tenants_notifies_both` |
| CR-03 | `worker.py:102`（`while True`）、`worker.py:43`（DLQ 的 TODO）、`settings.py` 的 `max_attempts` 从未使用 | P0 | 重试无上限、无退避、无 DLQ；畸形消息被吞 | 影响面：一个坏 endpoint 占满线程池（并发 8），所有租户的通知停摆；对下游是自我 DoS；可能性：任何一个客户的 webhook 宕机即触发；PR 说明里"重试到成功"是有意的，因此更需要指出 | 进程内最多 `max_attempts` 次 + 指数退避加抖动；仍失败则 `change_visibility` 退避重投；`receive_count >= max_receives` 进 DLQ；畸形/不可重试直接进 DLQ | `test_cr03_failing_downstream_is_bounded_and_dead_lettered`、`test_cr03_failed_message_backs_off_instead_of_being_redelivered_immediately`、`test_cr03_malformed_message_goes_to_dlq_instead_of_vanishing` |
| CR-04 | `config_store.py:30` | P0 | `tenant_id` 用 f-string 拼进 SQL | 影响面：租户 id 来自消息体，上游一旦被污染就能读出所有租户的渠道配置与 webhook secret；即使不是攻击，含 `'` 的租户名会让查询报错、告警丢失。可发现性：评审里一眼可见，测试里不会出现 | 参数化查询 `WHERE tenant_id = ?` | `test_cr04_tenant_id_is_data_not_sql`、`test_cr04_tenant_id_with_a_quote_does_not_break_lookup` |
| CR-05 | `dedup.py:14-23`、`worker.py:88,112` | P1 | 去重是"先 `seen`、发完才 `add`"，多线程共享 dict、无锁 | 同一告警的两份拷贝（PR 自己说生产者会重复发）并发处理会都通过检查 → 重复通知；`add` 里遍历删除在多线程下还可能 `KeyError`。影响面：重复通知而非丢失，所以 P1 | 原子 `claim(key)`（锁内检查并写入），失败 `release`；key 带渠道，部分失败重投只重试失败的渠道 | `test_cr05_concurrent_duplicates_send_once`、`test_cr05_redelivery_after_partial_failure_does_not_resend_to_the_channel_that_worked` |
| CR-06 | `senders/webhook.py:33` | P1 | `urlopen` 没有 `timeout` | 客户端慢/黑洞会让线程永久挂住；8 个线程挂住 = 整个 worker 停摆。比 CR-03 更隐蔽（没有日志、没有错误）。可能性高（客户 endpoint 不受我们控制） | `timeout=settings.webhook_timeout_s`；超时当作 `SendError` | `test_cr06_webhook_has_a_timeout` |
| CR-07 | `senders/webhook.py:31` | P1 | 日志打印整个 headers，含 `Authorization: Bearer <secret>` | secret 进入日志系统，影响面是所有有权读日志的人；一次性泄露难撤回 | 只记录 target/tenant/alert id；secret 不进日志，必要时脱敏 | `test_cr07_webhook_secret_is_not_logged` |
| CR-08 | `senders/email.py:24`、`senders/slack.py:24` | P1 | `except Exception: pass`/只记 debug，发送失败被当成成功 | 失败既不重试也不告警，渠道静默失效，和 CR-01 叠加后无任何证据；PR 里 stub 看起来无害，真实 transport 接上才暴露 | 转成 `SendError` 抛出，交给 worker 的重试/退避/DLQ | `test_cr08_slack_failure_is_reported_not_swallowed`、`test_cr08_email_failure_is_reported_not_swallowed`、`test_cr08_failed_slack_send_keeps_the_message` |
| CR-09 | `senders/base.py:13` | P1 | `format_message(alert, fields=[])` 可变默认参数 | 列表跨调用累积：**租户 A 的用户邮箱会出现在租户 B 的通知里**（跨租户数据泄露），并持续增长。看起来是 P2 的 Python 经典坑，但后果是泄露，所以升到 P1 | `fields=None` 再 `list(fields or [])` | `test_cr09_message_text_does_not_leak_between_alerts` |
| CR-10 | `queue.py:59,65,72`（diff 外） | P2 | receipt handle 就是消息 id，不是"每次投递一个" | visibility 过期后消息被 B 收到，A 慢了一步 `delete(old receipt)` 会删掉 B 正在处理的消息。需要超时与慢处理叠加才触发，所以 P2；但修了 CR-01 之后 visibility 的语义就依赖它 | 每次 `receive` 生成新 receipt（uuid），`delete`/`change_visibility` 按 receipt 匹配 | `test_cr10_stale_receipt_cannot_delete_a_redelivered_message` |
| CR-11 | `worker.py:81-82` | P2 | 把 UTC 字符串去掉 `Z` 变成 naive datetime，再减 `datetime.now()`（本地时间） | 非 UTC 主机上告警年龄偏差若干小时，误判 stale 而静默丢弃；生产全是 UTC 所以概率低；但测试机/开发机会不一致 | 解析为 aware（`+00:00`），与 `datetime.now(timezone.utc)` 比较 | `test_cr11_staleness_check_is_timezone_independent` |
| CR-12 | `worker.py:93` | P2 | 每条消息各查一次租户渠道（N+1） | 一批 10 条同租户 = 10 次查询；sqlite 现在不痛，换 Postgres 后是延迟和连接数放大器 | 每批按租户缓存一次，或 `IN (...)` 批量查 | `test_cr12_channel_config_is_fetched_once_per_tenant_per_batch` |
| CR-13 | `worker.py:69-112`；`tests/` | P2 | `process_message` 44 行做六件事；魔法数字（900/3600/3）散落；测试只有 happy path，没有任何失败路径 | 不是故障本身，但正是它让 CR-01/03/08 逃过了测试：评审里应当指出"没有测试覆盖失败路径"并要求补 | 拆成 解析/过滤/发送/收尾；阈值进 `Settings`；补 `tests/test_failure_paths.py`（solution 里有示例） | solution 自带 `tests/test_failure_paths.py`（3 个测试） |

## 评审中的"陷阱"与判断

- **红鲱鱼**：`except Exception: log.exception("worker error")`（`worker.py:57`）看起来像吞错，但那里是 `run_once` 的最外层兜底，不是 bug；`ThreadPoolExecutor` 并发本身没问题。
- **diff 外两条**：CR-02（`models.py`）、CR-10（`queue.py`）。只读 diff 的人会漏掉；能说出"我顺着 `dedup_key` 点进了定义"是加分项。
- **PR 描述里的"设计说明"本身就是评审线索**：`ack immediately`（CR-01）、`retried until they succeed`（CR-03）、`one worker process`（CR-05）、`DLQ is not wired up`（CR-03）。
- **优先级的可辩护性**：CR-09 可以辩护为 P2（教科书式小坑），但"后果是跨租户泄露"让它至少是 P1；说出理由比选对字母重要。
