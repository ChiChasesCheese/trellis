# 07 · Onsite · System Design（45 min）

> 事实层在 `loop/LOOP_GUIDE.md` §7。本章讲练法。

## 谁有这一轮

L2+ 一轮 45 分钟（真正设计 30–35 分钟）。**校招/实习通常没有**——设计能力会在 integration 和 coding 的追问里考。个别 L2/校招有报告。

工具是 **Whimsical**（在线白板），没有代码编辑器。全程口头 + 画框图。

## 这轮最容易被误解的一点

**题面是一大段业务描述，不给需求列表。** 有候选人在帖子里抱怨"题面不清"——那不是出题失误，**那就是考点**。

Exponent 的五维评分里，**problem framing 是第一维，API & data model 权重最高**：

| 维度 | 权重 |
|---|---|
| Problem framing | 入场券 |
| **API & data model** | **最高** |
| Failure modes & scale | 高（一手拒因就出在这） |
| Separation of concerns | 中 |
| Delivery（rollout / 测试 / 监控） | 中 |

不考"设计 Instagram"。全是支付域：webhook 投递、幂等支付 API、ledger、限流、订阅计费、Connect 分账。

## 45 分钟的主线（背下来）

1. **两句话复述** + 说出**不变量**：钱不丢 · 不双扣 · 账要平
2. **API 契约**：幂等键、错误码、版本、分页
3. **数据模型**：可变业务对象 vs **不可变 ledger**；金额用整数最小单位
4. **一致性**：DB 唯一约束是真相源，Redis 只加速
5. **失败模式**：重试 + 退避 + 抖动 · DLQ · outbox · saga · 熔断 · 租户隔离
6. **对账**
7. **可观测 + rollout**

前两步别省。**不先框需求就开始画图**是明确记录的挂点。

## webhook 题的四个必答追问

这题最高频，而且这四问被点名：

| 追问 | 答题要点 |
|---|---|
| 商户返 500 怎么办？ | 指数退避重试（Stripe 自己是最长三天）→ 超限进 DLQ → 商户后台可见投递历史 + 手动重发 |
| 商户 hang 住怎么办？ | 请求级超时 + 每商户并发配额 + 熔断，**防止一个商户拖垮整个投递池**（租户隔离） |
| SSRF 怎么防？ | 注册时校验目标不是内网/元数据地址，解析后再校验（防 DNS rebinding），出网走隔离的 egress 代理，只允许 HTTPS |
| exactly-once 能不能做到？ | **做不到**。诚实答"at-least-once + 消费端幂等"：事件带稳定 event id，商户按 id 去重；并且**不保证顺序**，所以不能用 `created` 排序或去重 |

一手拒因（Staff 面试官，webhook 题）：**"insufficient reasoning about failure modes and system abuse"** —— 前两问和第三问就是它说的那两件事。

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 单 region 单库 | 至少说出多可用区 + 读副本 + 故障切换，哪怕不深入 |
| 不先框需求就画 | 前 5 分钟只说话不画 |
| webhook 四问答不上 | 上表背下来 |
| 30 分钟讲完、没有 concern、仍被拒 | 讲完主线**主动抛权衡**："这个方案在 X 上有代价，如果流量到 Y 我会改成 Z" |

最后一条最反直觉：**讲得顺、讲得完、还是挂**。因为面试官期望的是一场讨论，不是一次演讲。

## 明天怎么练（具体到命令）

```bash
python3 loop/mock.py show sd01     # 只看题面
python3 loop/mock.py start sd01 -m 45   # 打印题面 + rubric，开始计时
```

练法（**不要直接看 model_answer**）：

1. 45 分钟自己画 + 出声讲（**真的录音或对着空气讲**，这轮全靠嘴）
2. 拿 `rubric.md` 给自己按五维打 1–4 分
3. 再读 `model_answer.md`，看差在哪一环
4. 过 `followups.md` 的 8+ 条追问，答不上的记下来

六道题：`sd01` webhook 投递 · `sd02` 幂等支付 API · `sd03` ledger · `sd04` 分布式限流 · `sd05` 订阅计费 · `sd06` 短题三连（Connect 分账 / feature flag / metrics）。

**sd01 至少练两遍**，它是最高频且四问最经典。

## 自检清单

- [ ] 拿到一段业务白话，我能在 5 分钟内说出功能需求 / 非功能需求 / 三条不变量
- [ ] 我先说 API 契约和数据模型，再画框图
- [ ] 我知道"不可变 ledger + 可变业务对象"这个组合以及为什么
- [ ] 我能说清 DB 唯一约束和 Redis 的分工
- [ ] webhook 四问我能各答 30 秒
- [ ] 我会主动抛出至少两个权衡，不等面试官问
- [ ] 我练过对着空气讲 30 分钟（这轮不写代码，全靠说）

## 对应材料

- 题目：`loop/rounds/07_system_design/sd01`–`sd06`（每题 prompt / rubric / model_answer / followups）
- 卡片：`loop/study/20-cards/stripe_api.md`（幂等、分页、限流、webhook 语义是设计题的原料）
- 素材：`loop/raw/system_design.md` §4（六大题中文模型答案）
- 事实与来源：`loop/LOOP_GUIDE.md` §7
