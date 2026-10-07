# REPORT · cb04_quarantine

> 由编排者代存（子代理被拒写 REPORT.md）；数字已由编排者重跑 3 次，结果一致：验收 38 passed · `IMPL=starter -m core` 19 failed / 19 deselected · starter 54 passed · solution 78 passed。

## Summary

`quarantine`：多租户钓鱼邮件隔离服务（"Report phishing" → 解析/查重 → 4 个 analyzer → QUARANTINE / RELEASE / NEEDS_REVIEW → mailbox 动作 + action log → 回执；sqlite；标准库 WSGI API）。题型 **fix-the-codebase**：`starter/` 带 6 处埋好的缺陷（自带 54 个测试全绿，缺陷只在 ticket 场景下暴露）。t1 找并修 bug（Prove-It）· t2 开放的 production-ready（排序与取舍）· t3 数千人报告同一封邮件时不垮并显示报告人数。

## 代码库地图（`starter/`）

| 模块 | 一句话 |
|---|---|
| `quarantine/cli.py`, `__main__.py` | `ingest` / `show` / `analyzers` / `serve`；`main(argv, out, mailbox)` 可注入 mailbox |
| `quarantine/app.py` | 组合根：`create_app(db_path, config_dir, fixtures_dir, clock, mailbox, url_lookup)` |
| `quarantine/config.py` | `Settings`、tomllib + 租户深度合并、严格校验；`IntakeSettings.max_links` 已定义但没人用 |
| `quarantine/models.py`, `errors.py`, `metrics.py`, `timeutil.py` | `Report`/`Verdict`/`Disposition`/`ReportStatus`；异常；计数器；aware-UTC 时间（`to_utc`、`iso`、`parse_rfc2822`） |
| `quarantine/intake/` | `parse_report`；`IntakeService.submit`（查重 → 分析 → 决定 → 入库 → 动作 → 回执）与 `_repeat` |
| `quarantine/analyzers/` | `Analyzer` + `@register_analyzer` + `AnalysisContext`；4 个 analyzer；`AnalyzerRunner`（计数钩子 `analyzer.run`） |
| `quarantine/lookups/` | `UrlLookup` 协议 + `FixtureUrlLookup`（含模拟供应商故障的 `unavailable` 主机）；`SenderIntel` |
| `quarantine/decision.py` | `decide`：最高分 + 租户阈值 → `Disposition` |
| `quarantine/actions/` | `Mailbox` 协议 + `FakeMailbox`（记录调用、可让回执失败）；`ActionService`；`notify.send_receipt`（同步，在请求路径里） |
| `quarantine/store/` | `connect`（`LockedConnection`：语句级加锁，让并发测试暴露的是逻辑竞态而不是 SQLite 误用；不是埋点）、`migrate`、`ReportRepository`、`ActionLogRepository` |
| `quarantine/api/` | `framework.py`、`app.py`（Bearer → tenant）、`testing.py`、`routes/reports.py` |
| `quarantine/legacy/regex_filter.py` | deprecated，无 import |
| `README.md` | **一处过时**：声称 `legacy/regex_filter` 在 analyzers 之前运行 |

## 规模（实测）

| 项 | starter | solution |
|---|---|---|
| Python 文件 / 行数 | 45 / 2,151（tests 552） | 45 / 2,626 |
| 全部文件 | 61 | 64（新增 3 个 migration） |
| 自带测试 | 54 passed，0.08 s | 78 passed，0.28 s |

## 埋点清单

### t1 planted bugs
| # | 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|---|
| B1 | 竞态 | `intake/service.py:IntakeService.submit`（find → 分析 → insert）；`0001_init.sql` 只有普通索引 | 新 migration 加唯一索引；`IntegrityError` → `DuplicateReport`，败者走已有 report 分支 | `threading.Lock`；"再查一次" |
| B2 | 跨租户 | `store/repositories.py:ReportRepository.get` 收了 `tenant_id` 却没用 | SQL 加 `AND tenant_id = ?`；GET 与 release 一并修好；grep 其余 `WHERE` | 在路由里手判，release 与 CLI `show` 仍泄露 |
| B3 | 时区 | `intake/parsing.py:_sent_at` 用 `.replace(tzinfo=None)`；`count_sender_reports` 按朴素时间比较 | `timeutil.to_utc` + `iso` | 窗口改 48 h 掩盖 |
| B4 | 吞异常 | `analyzers/link_reputation.py`：`except Exception: return Verdict(score=0)` | 去掉；`AnalyzerRunner` 统一捕获、`analyzer.error` 计数、inconclusive → `decide` 至少 NEEDS_REVIEW | 故障一律 QUARANTINE；`except: pass` |
| — | 必须复用 | `AnalyzerRunner`、`metrics.incr`、`decision.decide`、`store/migrations/`、`timeutil` | 统一处理；新 `0002_*.sql` | 每个 analyzer 各写 try/except；改 `0001` |
| — | 看起来像但不该改 | `legacy/regex_filter.py`；README 的 "pre-filter" | 不碰 | 以为它是漏判原因 |
| — | 模糊点 | 服务故障时放行/隔离/复核；泄露是否只在 GET | 问；默认 NEEDS_REVIEW；两条路径都查 | 直接 RELEASE |

### t2 production-ready
| # | 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|---|
| B5 | 非幂等 release | `actions/service.py:ActionService.release` 不查状态 | 条件更新 `set_status_if`，只有赢家调 mailbox；CLEARED → 409 | 只在 Python 里判状态（并发仍重复） |
| B6 | 连接泄露 | `cli.py:main`：`close()` 不在 `finally` | `try/finally` | 无测试可见，只能读代码发现 |
| — | 必须复用 | `errors.py`、`api/framework.py:BadRequest/Conflict`、`IntakeSettings.max_links` | `ValidationError` → 400；接上 `max_links` | 路由手写 400；常量 50 |
| — | 必须复用 | `ActionLogRepository`、`cli.main(..., mailbox=)`、migrations | outbox 表 + `drain-outbox` 命令 | 后台线程或重试装饰器；吞回执异常 |
| — | 看起来像但不该改 | `send_receipt` 调用点之外 / "顺手加鉴权" | 只把回执移出请求路径；鉴权写进 known gaps | 先做鉴权，没收口 |

### t3 burst scale
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `IntakeService._repeat`；`reports.verdicts` 已持久化 | 重复报告不再分析，已存 verdicts 就是缓存；只记录报告人 | `lru_cache` / 模块级 dict；线程池 |
| 必须复用 | `ReportRepository` + migrations；`Report.to_dict` | `report_reporters` 表（PK 含 tenant）+ 回填；`reporter_count` | 计数放内存；N+1 |
| 必须复用 | `metrics.get("analyzer.run")`、`FakeMailbox.calls_of` | 用已有钩子证明只分析一次、只隔离一次 | 自加全局计数 |
| 看起来像但不该改 | 去重键 `(tenant, message_id)` | 不动 | 按内容哈希合并（丢报告人） |
| 模糊点 | 同一人重复点击；后续报告是否改判定；每人回执；是否暴露名单 | 默认计一次、不重评估并说出口、每个新报告人一条回执、只暴露计数 | 悄悄放弃重新评估 |

## 验收测试清单

| ticket | core | stretch | regression | 合计 |
|---|---|---|---|---|
| t1 | 7 | 2 | 5 | 14 |
| t2 | 7 | 3 | 4 | 14 |
| t3 | 5 | 2 | 3 | 10 |
| 合计 | 19 | 7 | 12 | 38 |

只用已有入口：`create_app()`（注入 `mailbox`、`url_lookup`、`db_path`）、`TestClient`、`FakeMailbox`、`quarantine.metrics`、`cli.main`；新名字只有 ticket 点名的 `reporter_count`、`drain-outbox`。并发用例用线程 + 慢 lookup 拉宽 check-then-insert 窗口。B6 没有可观测症状，只在 walkthrough 与 known gaps；B3 只有 stretch 测试覆盖。

## solution 改动行数

`diff -ruN starter solution` = 1,186 行（增删 732，非测试 445、测试 287）。一次性实现三张 ticket，按文件人工归属：`store/repositories.py` 115（t1·t2·t3）· `cli.py` 57（t2）· `intake/parsing.py` 51（t2·t1）· `intake/service.py` 48 · `actions/notify.py` 48（t2）· `actions/service.py` 18（t2）· `analyzers/runner.py` 16（t1）· `api/routes/reports.py` 13（t2）· migrations `0002/0003/0004` 3/15/11（t1/t2/t3）· 测试 287。

## 最弱的两处

1. 每张 ticket 的改动行数是按文件人工归属，不是分步构建实测。
2. B6（连接泄露）无验收覆盖；B3（时区）只有 stretch 覆盖。
