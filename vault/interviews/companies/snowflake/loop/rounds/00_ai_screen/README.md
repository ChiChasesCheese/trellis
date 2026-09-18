# 00 · Chakra AI 语音筛（20 min）— 本轮全部材料在这个目录

> Snowflake GenSWE · Software Engineer - Backend · HackerRank Chakra 20 分钟 voice-to-voice · 截止 **2026-09-24 21:36 PDT**。
> 四段（邀请邮件原文）：experience & role-related background · applied scenarios · collaboration & decision-making · questions for us。一手报告 ×3：**只问 BQ + 项目，无 coding**；打分只读 transcript；JD must-have 加权。
> 口径：senior SDE —— 端到端 ownership、设计取舍、平台化、事故指挥、带人；每答命中 JD 线 **SQL · distributed systems · Java · database internals · large-scale production**。数字只说量级 + "roughly"。

## 读的顺序

| # | 文件 | 是什么 | 什么时候读 |
|---|---|---|---|
| 1 | `../../../../../core/playbooks/ai-voice-screen.md` | 机制：Reporter 只读 transcript；3/2/1/0；theoretical = Not Met；操作清单 | 第一遍 |
| 2 | `playbook.md` | 逐分钟剧本 · 60 s 自我介绍 · 段一/三怎么挑故事 · 危险追问 · 收尾 · 当天 | 第一遍 + 前一晚 |
| 3 | `stories.md` | 十个故事的英文首答（60–90 s）+ 追问版 + 追问弹药 | 反复 |
| 4 | `scenarios.md` | 12 道 applied scenarios 全文（Clarify → 3 步 → closest thing → trade-off） | 反复 |
| 5 | `questions.md` | **完整题库 79 题**：题面 → 故事 → 关键词提示（A 经历 17 · B 场景 18 · C 协作 20 · D 追问 12 · E 收尾 4 · **F 亲历 8**） | 抽练 |
| 6 | `bank.json` | 题库的机器版，`python3 loop/mock.py bq ai -n 5` 抽题 | 抽练 |
| 7 | `rubric.md` | Chakra 四档打分 + 自评 3/2/1 + 录音回听清单 | 自评 |
| 8 | `CARD.md` | 关键词卡：每题只留提示词，贴摄像头旁 / 手机 | 当天 |
| — | `../../../07-mock.md` | 20 分钟计时自测（题从本目录抽） | 前一晚 ×2 |
| — | `../../../04-answer-bank.md` | Snowflake 特定题 + 价值观×故事矩阵 + 数字卡 | 备查 |
| — | `../../../raw/chakra.md` · `../../../raw/emails.md` | 证据：Chakra 机制调研、邀请邮件原文 | 备查 |

## 命令

```bash
# 在 kit 根目录 vault/interviews/companies/snowflake
python3 loop/mock.py bq ai -n 5                 # 随机抽 5 题（q / principle / story / keys / source）
python3 loop/mock.py bq ai -n 8 --seed 7 -m 2   # 固定种子、每题 2 分钟
python3 loop/rounds/00_ai_screen/build_bank.py  # questions.md 改了之后重新生成 bank.json
python3 loop/rounds/00_ai_screen/build_bank.py --check   # 校验 bank.json 没过期
python3 loop/tree/check_tree.py --strict        # 知识树：本轮 skill → problems: [ai]
```

## 故事 ↔ 题的映射（一屏）

| 故事 | 一句话 | 主要接的题 |
|---|---|---|
| S1 Amex 结算管线 | good-funds model · COPY INTO → 6 append-only Streams → MERGE → UDTF FULL OUTER JOIN → Task AFTER A,B | A02 A06 A08 B02 B10 B12 |
| S2 Quality-check 框架 | contract-config + EXECUTE IMMEDIATE + trigger-status handshake；ADR strictest-wins | A05 A14 B08 B18 C04 C15 |
| S3 ACH NULL 传播 | 'BT_' \|\| NULL = NULL；UDF overload；postmortem；fail loudly | A03 B01 C13 |
| S4 AU Amex refund | 50 回复的跨团队争论 → 一条查询结束 | C02 C14 |
| S5 Interchange 数据源切换 | 静态拆分 vs 更聪明 fallback；同源 shadow；四层 MERGE；deploy ≠ release | A04 A10 B03 B09 B17 C01 |
| S6 Anomaly detector go/no-go | QA 6 merchants vs prod 18k；SQL pushdown 先行；gate | C03 C10 C11 B04 |
| S7 schema pool | zero-copy clone 池；prod-deployed SHA；agent 并行 | A13 C16 |
| S8 Terraform 7 分钟 RCA | outbound_privileges；主动指出未爆的同类风险 | C12 C17 |
| S9 Amex 出款延迟事故 | SLA 权威；region conditional > revert | B05 C05 C18 |
| S10 Billing-terms 复盘 | 推翻自己 10× 的 blast radius | C06 B09 |

## 面后复盘

2026-09-17 那场的转写、数字与逐题评审：`../../../debrief/2026-09-17-chakra/REVIEW.md`（结论：语法不是问题，headline 与证据词才是；实际是 14 问的 intake，不是四段式）。工具：`../../../../../core/debrief/README.md`。

## 面完回写

实际被问的题 + 追问 → `../../../02-process.md` 末尾「亲历」；新题追加进 `questions.md` 对应段并重跑 `build_bank.py`；被追到答不上的 → `stories.md` 追问版补一条；通用教训 → `../../../../../core/playbooks/ai-voice-screen.md`。
