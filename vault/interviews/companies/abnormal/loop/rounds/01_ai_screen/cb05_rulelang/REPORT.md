# REPORT · cb05_rulelang

> 由编排者代存（子代理被拒写 REPORT.md）；数字已由编排者重跑：验收 36 passed · `IMPL=starter -m core` 22 failed / 14 deselected · starter 39 passed · solution 69 passed。

## Summary

`rulelang`：多租户邮件安全检测引擎（事件 jsonl → `Detector` 注册表 → `Signal` → sqlite；`CommGraph` 记录谁给谁发过邮件；WSGI API；`python -m rulelang` CLI）。题型为算法型扩展：三张 ticket 各藏一个经典模式，难点是认出模式并挂在已有抽象上。t1 客户自定义规则（小语言：tokenizer + 递归下降 + 求值）、t2 检测器依赖（`Detector.requires` 已存在但 runner 不读，拓扑排序）、t3 被盗账号影响面（`CommGraph` 上带时间约束的 BFS）。

## 代码库地图（`starter/`）

| 模块 | 一句话 |
|---|---|
| `rulelang/cli.py`, `__main__.py` | `run` / `signals` / `detectors` / `serve`；`RulelangError` → `error: ...` + 退出码 2 |
| `rulelang/app.py` | 组合根：`create_app()` 返回 db + settings + `Pipeline` + WSGI app |
| `rulelang/pipeline.py` | `Pipeline.run/process`：detect → 存事件 → 更新图 → 存 signals；每租户一份 runtime |
| `rulelang/config.py` | `Settings`、tomllib 加载 + 租户覆盖深度合并、严格校验（未知 section/key = `ConfigError`） |
| `rulelang/models.py`, `errors.py`, `metrics.py`, `timeutil.py`, `addresses.py` | `Event`/`Signal`/`Severity`；异常；计数器；UTC 时间；地址/主机归一化 |
| `rulelang/intel.py` | `IntelStore`：bad hosts、域名年龄、已知供应商 |
| `rulelang/events/` | `load_events`/`parse_row`：坏行计数并跳过，别的租户的行跳过 |
| `rulelang/detectors/` | `Detector`（`name`/`kinds`/`requires`/`evaluate`）+ `@register_detector`；6 个检测器；`DetectorRunner`（按注册顺序，不读 `requires`） |
| `rulelang/graph/` | `CommGraph`：有向边（首次/最近联系、次数），`record`/`neighbors`/`first_contact` |
| `rulelang/store/` | `connect()`、`migrate()`、`EventRepository`、`SignalRepository`（都带 `tenant_id`） |
| `rulelang/api/` | `framework.py`、`app.py`（Bearer → tenant）、`testing.py`（`TestClient`）、`routes/signals.py` |
| `rulelang/legacy/yaml_rules.py` | deprecated 的 v0 规则格式（半个 parser，没人 import） |
| `README.md` | **一处过时**：声称检测器按依赖顺序运行 |

## 规模（实测）

| 项 | starter | solution |
|---|---|---|
| Python 文件 / 行数 | 43 / 2,020（tests 425） | 51 / 2,922 |
| 全部文件 | 56 | 64 |
| 自带测试 | 39 passed，0.10 s | 69 passed，0.14 s |

## 埋点清单

### t1 custom rules
| 类型 | 位置 | 正确做法 | AI 不看代码时的典型错法 |
|---|---|---|---|
| 必须复用 | `detectors/base.py:Detector / register_detector`、`detectors/runner.py:DetectorRunner.__init__` | 每条规则 = 一个 `Detector` 实例追加进 runner，产出同形 `Signal` | 新建 `RuleEngine`/独立结果通道 |
| 必须复用 | `config.py:_ALLOWED / build_settings`、`errors.py:ConfigError`、`cli.py:main` | `[rules]` 新 section，加载期编译；`ConfigError`（规则名 + 行列号）→ 退出码 2 | 新建 `rules.yaml` 加载器；只在运行时报错并被吞 |
| 必须复用 | `intel.py:IntelStore`、`addresses.py:host_of / domain_of / is_internal` | 字段求值走它们；未知域名年龄 = `None` = 不匹配 | 自己读 intel json、`urlparse`；`None < 7` 抛 `TypeError` |
| 看起来像但不该改 | `legacy/yaml_rules.py:parse_rule` | 不 import、不扩展 | 扩展这个"半个 parser" |
| 不问就会做错 | 加载期失败 vs 运行时跳过；未知年龄；作用于哪些事件；`any` 语义 | `interviewer.md` t1 ② | 运行时静默跳过；`None` 当 0 |
| 模式陷阱 | 字面量 | `and` 比 `or` 紧；`<=` 先于 `<`；列号；转义引号 | `eval()`；同级左结合；正则硬切 |

### t2 detector dependencies
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `Detector.requires`（已有、无人读）、`DETECTORS`（保序字典） | Kahn，同层保持注册顺序 | 新增 `priority` 字段或在下游打补丁 |
| 必须复用 | `DetectorRunner.__init__ / run`、`DetectorContext.signals` | 构造时排序，运行时跳过 | 每个事件重新排序 |
| 必须复用 | `ConfigError`、`metrics.incr`、`DetectorSettings.disabled` | 环/未知依赖 → `ConfigError` 点名；跳过计数；禁用上游 → 下游跳过 | `graphlib.CycleError` 冒泡；用缺失数据继续判断 |
| 看起来像但不该改 | `detectors/__init__.py` 的 import 顺序；README | 调 import 顺序不是修复 | 把 `new_sender` 排前就收工 |
| 不问就会做错 | 上游禁用/崩溃/"没触发"的区别 | `interviewer.md` t2 ② | 把"没触发"当失败 |

### t3 blast radius
| 类型 | 位置 | 正确做法 | 典型错法 |
|---|---|---|---|
| 必须复用 | `CommGraph.neighbors / Edge`（`first_ts`/`last_ts`） | 只用 `neighbors`，边条件 `last_ts >= arrival` | 每跳回查 events 表；用 `first_contact` 做时间过滤 |
| 必须复用 | `config.py`、`OrgSettings.internal_domains`、`addresses.py:is_internal / normalize_address` | `[blast_radius] max_hops`；外部 = 不在 `internal_domains` | 常量读跳数；大小写敏感 |
| 必须复用 | `api/framework.py:route / BadRequest`、`routes/signals.py`、`timeutil.parse_ts` | 新路由注册；非法 `since` → 400 / 退出码 2 | 手写错误 body；500 |
| 不问就会做错 | `since` 含不含当刻；只走出边；外部展不展开；跳数怎么数 | `interviewer.md` t3 ② | 无 `seen` 的递归 DFS；外部被展开 |
| 模式陷阱 | 字面量 | 入队时标 `seen`；`hops == max_hops` 只列不展开 | 出队才标 `seen`；截断错一层 |

## 验收测试清单

| ticket | core | stretch | regression | 合计 |
|---|---|---|---|---|
| t1 | 9 | 4 | 2 | 15 |
| t2 | 6 | 2 | 2 | 10 |
| t3 | 7 | 2 | 2 | 11 |
| 合计 | 22 | 8 | 6 | 36 |

只经由已有入口与 ticket 点名的新接口（`[rules]`、`GET /blast-radius`、`blast-radius` 子命令、`[blast_radius] max_hops`）。t3 响应形状、t1 列号基准由测试放宽。

## solution 改动行数

`diff -ruN starter solution -x __pycache__ | wc -l` = 1,125（增删合计 927）。按 ticket 近似：t1 ≈ 565（源码 ≈ 445、测试 ≈ 120）· t2 ≈ 150 · t3 ≈ 210。

## 最弱的两处

1. t3 的到达时间只是下界（`CommGraph` 只存 `first_ts`/`last_ts`），BFS 先到先得，可能漏掉只经由较晚路径可达的人；stretch 只覆盖单次联系的边。
2. t1/t3 的响应与语法细节靠测试容忍或由 `interviewer.md` 固定。
