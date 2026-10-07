# cb02_insiderwatch · REPORT

## Summary

`insiderwatch` 是一个只用标准库的 Insider Risk 检测后端：M365 / Okta / Slack 审计日志经 `Connector` 规范化成 `Event` → `@signal` 注册的信号读 SQLite 里的个人基线与 HR 名册、逐用户逐日产出 finding → `scoring` 乘配置权重 → 超阈值成为 `Alert` → `Notifier`。
在 `fixtures/raw`（`--until 2026-09-30`）上：starter 产生 51 条告警（alice 3、henry 48）；solution 产生 59 条告警、8 个 case、9 条 outbox 消息。
三张 ticket：t1 离职前数据外泄（团队核心场景）· t2 告警归并成 case（分析师疲劳）· t3 接入 Google Drive 审计日志（新数据源）。

## 代码库地图（`starter/insiderwatch/`）

| 模块 | 一句话 |
|---|---|
| `cli.py`、`__main__.py` | 子命令 replay / alerts / outbox / risk / export / check |
| `config.py` | frozen `Config`、TOML 覆盖、feature flags |
| `events.py` | `Event`、`Action` 枚举、`normalize_user`、`is_external`、`day_end` |
| `timeutil.py` | `parse_ts`、business hours、`daterange` |
| `db.py` + `migrations/0001..0004` | 编号迁移；约定"never edit an applied migration" |
| `connectors/base.py` | `Connector`、`@register_connector`、`drop()` + `ConnectorStats`；`m365_audit`、`okta`、`slack_audit` |
| `baselines/{store,stats}.py` | 滚动日统计 mean/std/p95；冷启动时 `get` 返回 `None` |
| `signals/` | `base.py` + `volume_spike`、`off_hours_activity`、`unusual_login_location` |
| `scoring.py` | `score_finding`、`severity_label`、衰减、`user_risk` |
| `alerts/{models,store}.py`、`notify/` | `Alert`、`AlertStore`；`Notifier` 协议、console 与 Slack-outbox |
| `hr/{roster,org}.py`、`pipeline.py` | 名册；逐日 replay，watermark 保证增量与幂等 |
| `report.py`、`export.py`、`check.py`、`legacy/dlp_rules.py` | 报表、导出、自检；deprecated 的旧 DLP 规则（README 仍提到它，故意过时） |

## 规模（子代理实测；编排者复核 gate）

| 量 | starter | solution |
|---|---|---|
| `.py` 文件 / 行数 | 45 / 2,074（包本身 1,510） | 51 / 2,539 |
| 自带测试 | 53 passed，1.6 s | 71 passed，3.1 s（+18） |
| 文件总数（含 fixtures/SQL/文档） | 62 | — |

`diff -ruN starter solution` 改动 410 行：t1 ≈ 113 · t2 ≈ 194 · t3 ≈ 103（只计生产代码约 66 / 105 / 62）。

## 埋点清单

| ticket | 必须复用 | 像但别碰 | 不问就会错的模糊点 | AI 的典型错法 |
|---|---|---|---|---|
| t1 | `@signal` 注册 + `signals/__init__` 的 import；`BaselineStore.get`（本人基线，`None` = 冷启动）；`signal_weights` 与 `scoring`；HR roster 与 `Action` | `legacy/dlp_rules.py`（500 MB 全局规则）、`volume_spike` | 窗口多长、哪些动作算"带走数据"、无基线的新人、离职后仍有活动 | 单测过但 replay 没加载该信号（忘 import）；全局阈值误伤 bob；漏配权重落到默认 0.2 而低于告警阈值；逻辑写进 `pipeline.py` |
| t2 | 新迁移 `0005_cases.sql`；`severity_label` + config 窗口；pipeline 里的 `Notifier` 调用点；`COMMANDS` 表与 `InsiderWatchError` | `notify/slack_webhook.py` 的 outbox、`alerts` 表与命令 | 事件的定义与窗口、取 max 还是 sum、关闭后再有告警是否重开、何时通知 | 改 0002 迁移；查询时临时分组；在 notifier 里去重；严重度取平均 |
| t3 | `Connector`（`parse_page` / `normalize` / `drop`，分页在基类）；注册 import；`parse_ts`；`is_external` + `internal_domains`；已有 `Action` | `slack_audit` 的 epoch 处理、`okta` | 什么算外部分享、view/edit/rename 怎么处理、一个 item 多个 event、`intValue` 是字符串 | 重写 fetch；忘 import；用 `fromisoformat`；新增 `Action`；只读 `events[0]` |

## 验收测试（`grep` 实测）

| ticket | core | stretch | regression | 合计 |
|---|---:|---:|---:|---:|
| t1 | 6 | 2 | 2 | 10 |
| t2 | 6 | 3 | 2 | 11 |
| t3 | 7 | 1 | 2 | 10 |
| 合计 | 19 | 6 | 6 | 31 |

- 只经由 CLI 子进程（JSON 输出）测试，不依赖内部名字。ticket 点名的接口：`alerts --user/--json`；`cases [--user] [--json]`（键 `id`/`user`/`status`/`severity`/`alerts`）、`cases close <id>`；数据源名 `gdrive`。
- 负例（bob / dave 不该报）先断言 carol / erin 被抓到，所以在 starter 上也是红的。
- 编排者 gate（`tools/verify_suites.py`，2026-10-06）：acceptance/solution 31 passed · starter core 19 failed · starter 自带 53 passed · solution 自带 71 passed → **OK**。

## 已知的弱点（练习时心里有数）

1. **t1 依赖调过的夹具**：solution 在某日计数超过 `max(1.25·p95, p95+0.5)` 时标记；bob / dave / carol 的数据让 z-score、p95 等合理规则结论一致，但"在本人 p95 附近更激进"的设计仍可能让"bob、dave 不报"失败——若你的 core 只挂这两条，先看你的阈值是不是太贴基线，而不是急着认为测试错了。
2. **t3 的 regression 写死了各数据源计数 `(1410, 257, 25)`**；t2 的 stretch 假设 case 窗口 ≥ 24 h（夹具里第二波在第一波 22 h 后）。
