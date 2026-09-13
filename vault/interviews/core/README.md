# core/ — 核心能力

与公司无关、每次面试都要用、每次面完都要回写的四样东西。公司目录（`../companies/<co>/`）只链接这里，不复制。

| 目录 | 是什么 | 什么时候改 |
|---|---|---|
| `resume/` | `resume.tex` 唯一源 + 投递 PDF + CHANGELOG | 改简历时；投递前核对数字口径 |
| `stories/` | `evidence-base.md`：Chi 画像 + S1–S9 旗舰故事（每个：一句话 → 动作 → 量化 → 证据锚点）+ 诚实红线；`resume-evidence-map/`：四个技术主题的 baseline → 看齐标杆 → 知识点 → 面试话术 | 有新故事 / 新数字时；面完一轮把被追问的细节补进对应故事 |
| `answers/` | 逐题答案手册 dim1–dim6：每题 A（影响导向 60–90 s）+ B（技术展开）。原为 Stripe HM 轮写的，但题目本身与公司无关 | 某公司新问了一道通用题，答完写回这里而不是公司目录 |
| `playbooks/` | 按轮次的通用打法（形式 · 评什么 · 挂点 · 备考动作）。目前：`ai-voice-screen.md`。其它轮次先看 `../companies/stripe/loop/LOOP_GUIDE.md`（最完整的实例），抽象出来的部分再搬进来 | 第二家公司遇到同类轮次时，把 Stripe 特有的部分剥掉后搬入 |

## 故事索引（细节见 `stories/evidence-base.md`）

| ID | 一句话 | 最常回答 |
|---|---|---|
| S1 | AMEX GRRCN 端到端管线，Ruby→Snowflake 迁移，21.96M 笔 / $138.6B | 最难项目 · 端到端 ownership · 迁移 |
| S2 | Quality-Check & Handshake 框架 + 自我修正 ADR | 架构决策 · 定标准 · 说服团队 |
| S3 | ACH fee-calc 生产事故 RCA（`'BT_' \|\| NULL`） | 最难 bug · on-call · 无授权影响他人 |
| S4 | AU Amex refund fee RCA（PM 正式 escalate） | 跨团队协作 · go-to person |
| S5 | Net Settlement Pricing，$55B+ TPV / $450M-月 float，shadow-run 0.224% | 最大业务影响 · 模糊性 · promotion |
| S6 | Fee Anomaly Detector 接管 + ROI go/no-go gate | staff 级判断 · 优先级取舍 · 敢说不 |
| S7 | snowglobe-tools：自发的 schema pool 让多 agent 并行 | 主动性 · craft · AI-native 工作流 |
| S8 | Terraform grant-ownership 7 分钟 RCA | 快速 debug · unblock 他人 |
| S9 | DoorDash Amex 出款事故，被指定 fix owner + SLA 权威 | incident · 跨团队 · 领域权威 |

## 诚实红线（所有答案共用，摘自 evidence-base §3）

- 已确认数字直接用：$138.6B / 21.96M、$55B TPV、$450M/月、196 merchants / $11.3M/day、13.7M 行 / 0.224%。
- 未确认用 `【预估：…】` / `【待 Chi 确认：…】`。简历上的 `$600B+`、`Sentry`、intern 的 `Kafka in K8s` 三处口径未闭合。
- 不编造 PR review 记录、1:1 对话、不存在的项目。带教 Ziyang 的框定是 domain-ownership，不是 code-review trail。
