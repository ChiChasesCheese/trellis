# walkthrough · cr01 alert fan-out（45 分钟）

真实面试的形态（#8496901 Round 4、1p3a 2025-10）：先给你一个小仓库做 code review，开场约 20 分钟讨论你的 comments，然后转到"扩展 + 规模"。本练习按 **45 分钟**切：

| 分钟 | 做什么 |
|---|---|
| 0-5 | 读 `PR.md`，圈出作者自己说的"设计决定"（它们是线索，不是答案） |
| 5-25 | 读 `pr.diff`，按下面的顺序；边读边写评论（带 file:line、优先级） |
| 25-32 | 让 Claude 复核你的清单（见下），把 AI 的发现并进来，删掉假阳性 |
| 32-35 | 写 60 秒口头总结，先 P0 |
| 35-45 | 第二部分：`followups.md` 里抽 3-4 个追问大声回答 |

## 1. 读 diff 的顺序

1. `worker.py`：数据流的主干。先问"消息的生命周期"——什么时候收、什么时候 ack、失败去哪（CR-01、03、05、11、12、13）。
2. `senders/`：每个渠道的失败语义和日志（CR-06、07、08、09）。
3. `config_store.py`：输入从哪里来、怎么进 SQL（CR-04）。
4. `dedup.py`：并发与 key 的语义（CR-05），**然后点进 `Alert.dedup_key` 的定义**（diff 外，CR-02）。
5. diff 里没有但被调用的 `queue.py`：`delete` / `change_visibility` 的契约（CR-10）。
6. `tests/`：看缺什么，而不是看有什么（CR-13）。

## 2. 给 Claude 的评审提示词

```
Review this diff for correctness under concurrency, failure modes, security and tenant isolation;
cite file:line; rank by blast radius. Follow every function the diff calls into, even if it is
outside the diff (models.py, queue.py), and say which findings you could not confirm by reading.
Separate "will break in production" from "style".
```

再追问两轮：`What happens to the message if the process is killed between line X and line Y?` 与 `Which of these would a unit test have caught, and which would not?`

## 3. 怎么复核 AI 的发现

- **常见漏报**：diff 外的问题（CR-02、CR-10）；"PR 描述里写了的设计决定"（AI 倾向于把它当成合理前提）；跨文件的组合效应（CR-01 + CR-08 叠加 = 静默丢失）。
- **常见假阳性**：把 `run_once` 里的 `except Exception: log.exception` 当成吞错；"ThreadPoolExecutor 不是线程安全"之类泛泛而谈；对 sqlite `check_same_thread=False` 大做文章（队列和配置都包了锁/读多，不是这次的重点）；把 stub transport 的 `log.info` 当成泄露。
- **复核方法**：每条 AI 发现都要求你能写出"一个会失败的最小测试"。写不出来的发现降级或丢掉。本练习的 `acceptance/` 就是这样一组测试：先读懂每个测试为什么在 starter 上红。
- **优先级不要照单全收**：AI 常把 P2（魔法数字、函数过长）排得很靠前；让它按"丢数据 > 泄露 > 重复 > 性能 > 风格"重排。

## 4. 评论怎么写（英文示例）

**P0（CR-01）**
> `worker.py:52` **[P0 · data loss]** We delete the message before sending, so any crash, OOM kill or deploy between here and the send loses the alert permanently, and nothing in the logs will show it. Please ack only after every channel has delivered (or been dead-lettered), and let the visibility timeout handle redelivery. A test that asserts the message is still in flight while `send()` runs would pin this down.

**P1（CR-06）**
> `senders/webhook.py:33` **[P1 · availability]** `urlopen` has no timeout, so one unresponsive customer endpoint pins a worker thread forever; with 8 threads, eight such alerts stall every tenant. Suggest `timeout=` from settings and treating a timeout as a `SendError` so it goes through the normal retry/backoff path.

**nit（CR-13）**
> `worker.py:69` **[nit]** `process_message` does parsing, filtering, dedup, lookup, sending and bookkeeping in 44 lines. Not blocking, but splitting it would make the failure paths testable, which is exactly where the tests are thin today.

## 5. 60 秒口头总结模板

> "I found four blockers. First, we ack before we send, so a crash loses a security alert silently. Second, the dedup key omits the tenant, so one customer's alert can suppress another's. Third, retries are unbounded with no backoff and no DLQ, so one bad endpoint can starve every tenant. Fourth, the tenant lookup builds SQL with an f-string. Beyond those, the main follow-ups are the webhook timeout, the secret in the logs, swallowed errors in the Slack and email senders, and a mutable default that leaks one tenant's user into another's message. I'd merge after the four blockers are fixed with tests for the failure paths, and handle the rest in a follow-up. Happy to talk about how this behaves at ten times the volume."

中文要点：先说结论（几个阻塞项）→ 每个一句话 + 后果 → 其余按组带过 → 给出合并条件 → 主动引到规模话题。
