# cb03_vetting · REPORT

## Summary

`vetting` 是候选人身份欺诈检测（对应 Abnormal 的 Infiltration Prevention，Chi 申请的团队）的标准库实现：Greenhouse 申请与 IdP 登录 → `Identity` + `Observation` → 注册的 signals（`voip_phone`、`ip_geo_mismatch`、`resume_name_mismatch`、`disposable_email`、`vpn_hosting_ip`）→ scoring → 分档推荐（HIGHLY_RECOMMENDED / RECOMMENDED / NONE）+ 证据时间线 → API / CLI。租户 acme、globex。
三张 ticket：t1 协同申请者关联（"one node in a campaign"）· t2 接入 Workday 数据源 · t3 用审核员的 disposition 降低重复误报。

## 代码库地图（要点）

接缝：`normalize.py`（E.164、/24、邮箱 key、姓名）· `@register_source` · `@register_signal` · `settings.py` + `config/default.toml`（`_SECTIONS` 注册配置段）· 按租户的 repositories · `SOURCE_LABELS` · `Finding.subject`。
噪音：`legacy/blocklist.py`（deprecated，无人 import）；README 两处过时（说权重在 `vetting/weights.py`，实为 `config/default.toml`；把 blocklist 画成管线一环）；夹具含坏记录、孤立 IdP 事件与 Workday 样本。

## 规模（子代理实测；编排者复核 gate）

| 量 | starter | solution |
|---|---|---|
| `.py` 文件 / 行数 | 45 / 2,228（包 1,748 · 测试 480） | 50 / 2,702 |
| 文件总数 | 62 | 67 |
| 自带测试 | 52 passed，0.6 s | 64 passed，1.3 s |

`diff -ruN -x __pycache__ starter solution | wc -l` = 731。每张 ticket 单独施加到 starter 的改动：t1 310 行（tests 127）· t2 259（141）· t3 299（95）（共享文件分别计入，三者之和 > 731）。

## 埋点清单

| ticket | 必须复用 | 像但别碰 | 模糊点 | AI 典型错法 |
|---|---|---|---|---|
| t1 | `normalize.phone_e164 / ip_prefix24 / email_key`；`ObservationRepository.list_by_kind`；`@register_signal`；`[correlation]` 配置段（`settings._SECTIONS` + `config/default.toml`） | `legacy/blocklist.py` | 常见共享值（NAT IP、招聘代理电话）不能单独定罪；是否跨租户；号码前缀长度 | 用 `ObservationRepository.find()` 精确匹配原始值，漏掉格式变体；单一共享属性就关联 |
| t2 | `Source`、`@register_source`、`observe()`、`bad_record()`、`parse_ts`、`Identity.make_id`、`raw_ref` 约定（重复投递去重）、`SOURCE_LABELS` | `signals/`、`pipeline.py` | 什么算重复；缺字段只丢该观测；分机号不进电话号码 | 改 signals 适配 Workday 字段；整条记录因缺邮箱丢弃；时区未转 UTC |
| t3 | disposition 历史；`Finding.subject`；`scoring` + `Pipeline.evaluate`；`[feedback]` 配置段 | 全局权重；`legacy/blocklist.py` | 降权还是隐藏；escalated 过的值不降权；只对孤立弱信号降权；租户隔离 | 全局关掉 signal；直接删 finding（失去证据）；被 cleared 一次就永久洗白 |

## 验收测试（34）

| ticket | core | stretch | regression |
|---|---:|---:|---:|
| t1 | 7 | 2 | 4 |
| t2 | 6 | 2 | 3 |
| t3 | 5 | 2 | 3 |
| 合计 | 18 | 6 | 10 |

只经由 `vetting.cli.main(["--db", …, "ingest", …])`、`create_app(db)` + `TestClient` 与 `/reviews` 端点测试；t2 读 starter 自带的 `fixtures/workday/`。
编排者 gate（`tools/verify_suites.py`，2026-10-06）：acceptance/solution 34 passed · starter core 18 failed（0 passed）· starter 自带 52 passed · solution 自带 64 passed → **OK**。

## 已知弱点

1. **虚构数据容易意外重合**：555-01xx 号码与三个文档 /24 网段让"同号段 / 同 /24"的意外重合比真实数据多；验收用了刻意分开的区号。若你的 t1 只凭号段一项就关联，可能被夹具里的意外重合绊倒——这本身也是"单一共享属性不定罪"的提醒。
2. t3 只检查推荐等级下降、finding 与证据仍在、以及 findings 里出现子串 "cleared"（不钉死措辞）；t2 依赖 starter 的 Workday 夹具与 Greenhouse JSON 形状。
