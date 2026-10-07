# 00 · 精要：在陌生代码库里 10 分钟找到扩展点（可迁移，比任何一题都重要）

> 本 kit 的覆盖率只量得到"报道过的那份代码库"。真实面试的代码库很可能不同——**能迁移的是这一页**：认出扩展点的形状、知道每种 feature 该挂在哪、知道 AI 不看代码时会怎么做错。
> 每节：**识别信号 → 正确挂法 → AI 的典型错法 → 一句英文口播**。练习对应：`loop/rounds/01_ai_screen/cb0*`。

## 1. 十分钟读代码的顺序

1. **README / CLAUDE.md / CONTRIBUTING**（1 min）：约定、命令、哪些过时。
2. **入口**（2 min）：`__main__.py`、CLI、`app`/`router`、`pipeline.run`——从入口往下看一层，不往深看。
3. **数据模型**（2 min）：`models.py` / `events.py` 的 dataclass——系统里流动的是什么。
4. **扩展点**（3 min）：搜 `register`、`Base`、`ABC`、`Protocol`、`@`、`REGISTRY`、`plugins`、`hooks`、`subscribe`。
5. **配置与存储**（1 min）：`settings`、`config`、`*.toml`、`migrations/`、`repository`。
6. **跑一次**（1 min）：测试 + README 里的 CLI。说出心智模型。

搜索语句（VS Code `Ctrl/Cmd+Shift+F` 或让 Claude 跑）：`register_|Registry|ABC|Protocol|plugin|hook|subscribe|publish|settings|tenant|migrat|deprecated|TODO`。

## 2. 七种扩展点与"该挂在哪"

| 形状 | 识别信号 | 新 feature 正确挂法 | AI 不看时的典型错法 | 口播 |
|---|---|---|---|---|
| **注册表 / 插件** | `@register_x`、`REGISTRY: dict`、`Base` 子类、`entry_points` | 新类 + 装饰器注册；不改调度代码 | 在调度循环里加 `if name == ...` | "Detections are registered with `@register_rule`, so a new one is a new class, not a change to the engine." |
| **硬编码的流水线 + 未被使用的基类** | `service.py` 里 if/else 依次调用；旁边有个 `Enricher` ABC；`TODO: make configurable` | 让已有基类成为发现与注册机制；内置实现也走同一机制；依赖用 `requires` 拓扑排序 | 新造一个 `PluginManager` 和第二套接口 | "There's already an `Enricher` base class that nothing uses for discovery — I'll make that the plugin contract instead of inventing a second one." |
| **分层配置**（default + tenant 覆盖） | `config/default.toml`、`tenants/<t>.toml`、`Settings` dataclass + 校验 | 新键加进 `Settings`（带默认值与校验），读 settings | 新建 JSON 文件 / 模块级常量 / 环境变量 | "Thresholds go into tenant settings with a default, so it's a config change per customer, not a deploy." |
| **Repository + migrations** | `repositories/`、`migrations/000N_*.sql`、所有查询带 `tenant_id` | 新表 = 新 migration 文件；新查询进 repository，带 tenant | 直接 `sqlite3.connect` 写 SQL；改已有 migration；漏 tenant 过滤 | "New table means a new migration, never editing an old one, and every query goes through the repository so tenant scoping is enforced in one place." |
| **策略层 / 决策点** | `policy.py`、`threat.py`、`scoring.py` 把信号合成结论 | 跨规则的横切决策（抑制、allowlist、降权）挂在**命中之后、出结论之前**的这一层 | 在每条规则里加判断 | "Suppression is a policy decision, so it belongs after rules fire and before alerts are created — not inside every rule." |
| **事件总线 / 任务队列 / outbox** | `events.publish`、`subscribers/`、`jobs.enqueue`、`outbox` 表 | 副作用（通知、webhook）订阅事件 → 入队 → worker 执行（重试/退避已有） | 在请求处理函数里同步发 HTTP | "I won't call the webhook inside the request; there's a job queue with retries, so the subscriber just enqueues." |
| **中间件 / 装饰器横切** | `middleware.py`、`require_role`、`errors.py` 统一错误形状 | 新端点用已有认证、角色装饰器、错误形状、分页工具 | 新端点自己解析 token、自己拼错误 JSON、用 OFFSET | "The new endpoint goes through the same auth middleware and error shape as the others." |

## 3. 模糊 feature 的四类隐藏期望（安全产品）

1. **误报 vs 漏报**：谁付代价？默认偏向"少打扰但不漏 CRITICAL"。被抑制/降权的东西**留痕**（审计、计数），不是静默丢弃。
2. **租户隔离**：每个配置、查询、缓存 key、关联都带 tenant；跨租户关联需要明确授权。
3. **攻击者会利用你的 feature**：allowlist 不该压过恶意附件；审核"cleared"不该让同一号码永久洗白；插件异常不能拖垮管线。
4. **幂等与重复**：重复投递、重复报告、重复运行不产生重复副作用。

## 4. 与 AI 协作的三条规则

1. **先让它看，再让它写**："Find the existing pattern for X and cite files" → 再 "follow that pattern"。官方原话："AI doesn't know what's already in the codebase unless you tell it to look."
2. **计划里写检查点**（Shrivu："defining … the 'inspection checkpoints' where it needs to stop and show me its work"）：M1 完成就停，跑、演示、再继续。
3. **审在 right altitude**：方法对吗 · 集成对吗 · 要紧的情况覆盖了吗。改掉一处并说出来——这是 ownership 的证据。

## 5. 收尾的证据（"Make Every PR Prove Itself"）

演示时给出：真实入口的输出（CLI / API 响应里的新字段 / 日志行）+ 新增测试名 + 全量测试结果 + known gaps 三条。
