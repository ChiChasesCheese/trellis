# REPORT · cr01 alert fan-out

## 规模（命令实测）

| 项 | 数字 |
|---|---|
| starter Python 行数（含测试） | 706（`find starter -name '*.py' \| xargs cat \| wc -l`），22 个 .py 文件 |
| solution Python 行数 | 823 |
| starter 自带测试 | 13 个，全绿，0.03 s |
| solution 自带测试 | 16 个，全绿 |
| `pr.diff` | 580 行，18 个文件，+388 / -2 |
| acceptance | 24 个测试：core 8 · stretch 11 · regression 5 |

## 问题分布

13 条：P0 4（CR-01 至 CR-04）· P1 5（CR-05 至 CR-09）· P2 4（CR-10 至 CR-13）；其中 2 条在 diff 外（CR-02 `models.py`、CR-10 `queue.py`）。完整表见 `REVIEW_KEY.md`。

## 验收清单

- [x] `python3 tools/verify_suites.py . "loop/rounds/03_code_review/cr01*"` 打印 `OK  cr01_alert_fanout`：solution 上 acceptance 24/24；starter 上 `-m core` 8 个全红；starter、solution 自带测试全绿。
- [x] 每个 P0 至少一个测试（CR-01 2 · CR-02 1 · CR-03 3 · CR-04 2）；P1 全部有测试（CR-05 2 · CR-06 1 · CR-07 1 · CR-08 3 · CR-09 1）；P2 中 CR-10/11/12 有测试，CR-13 以 solution 的 `tests/test_failure_paths.py` 体现。
- [x] 测试只经过包的公共入口（`Worker.run_once` / `process_message`、`Queue`、`ConfigStore`、`*Sender`）；starter 上的热循环用 `BaseException` 的 `Stop` 打断，保证红而不挂。
- [x] 全是文档网段/域名（`hooks.example.com`、`example.com`），无网络。

## 每个 P0 的"为什么是 P0"

- **CR-01 先 ack 后处理**：丢的是安全告警；每次部署/崩溃都会触发；丢了之后没有任何痕迹，无法事后发现。三个维度同时最高。
- **CR-02 去重 key 不含租户**：多租户产品里的跨租户影响，且是"静默不通知"而不是"报错"；自增 id 碰撞必然发生；必须点进 diff 外的定义才看得到。
- **CR-03 无限重试、无退避、无 DLQ**：一个客户的 endpoint 故障就能占满共享线程池，让所有租户停摆（自我 DoS）；PR 描述里把它写成了优点，评审要敢于否定。
- **CR-04 SQL 拼接**：租户 id 来自消息体，可读出其他租户的配置和 webhook secret；普通的含引号租户名也会让查询报错丢告警。

## 本练习的局限（诚实记录）

- 队列、去重缓存都是进程内/sqlite 的简化，真实系统是 SQS/Kafka + Redis；followups 里讨论了差异，但测试不覆盖多进程。
- solution 没有修的已知项：visibility timeout 与最坏处理时间（followups F4 的 47 s 计算）、按租户的 bulkhead（F3）。它们是第二部分的讨论题，不是评审必须发现的缺陷。
