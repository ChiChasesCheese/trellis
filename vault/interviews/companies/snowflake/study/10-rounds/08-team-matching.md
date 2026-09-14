# 08 · Team Matching（GenSWE 最后一步）

> 事实层在 `../../loop/LOOP_GUIDE.md` §9；题库与反问 `../../loop/rounds/08_team_matching/`。

## 这轮到底考什么（一句话）

**团队要不要你，以及 headcount 还在不在。** 一手：技术全过 → HM 对话 → 原 headcount 被占 → 新 HM 重面 → 10+ 天无回音；Snowflake 员工回复 "recruiting resources are spread thin"。

## 提前做的三件事（不是这一轮才做）

1. **电面阶段就问 recruiter**：在匹配哪些 org？headcount 是否已批？team matching 在 onsite 前还是后？
2. **准备三个方向**，每个一句理由：tasks / Dynamic Tables（重度用户的痛）· billing / metering（金融级对账 → 计量级对账）· FDB / Unistore / Postgres（结算 OLTP 真实负载）。
3. **每个方向准备一个公开的真问题**（`../../../06-questions-to-ask.md` §C）：Execution Anchor 的 1% 转移路径怎么测 · Adaptive Refresh 的信号 · 多模型路由后的成本归因。

## 对话中

- 先听团队 scope，再把自己做过的事映射上去（"the closest thing I've built is…"）。
- 直接回答 on-call 与 RTO；用真实 on-call 经历（S3/S9）。
- **最后必问**："Is the headcount for this role approved, and what's the timeline after today?"

## 会后

- 24 小时内给 recruiter 发一句：对这个组的兴趣 + 一个具体理由。
- 5 个工作日无回音就礼貌跟进一次；10 天再跟进并问是否并行匹配其他组。

## 练法

```bash
python3 loop/mock.py bq team -n 3 -m 3
```
对 `../../loop/rounds/08_team_matching/rubric.md` 四维打分；目标是"HM 会后能一句话推荐你"。
