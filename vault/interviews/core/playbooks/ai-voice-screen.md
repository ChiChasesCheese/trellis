---
title: Playbook · AI 语音筛
aliases:
  - AI voice screen
  - ai-voice-screen playbook
tags:
  - interview/playbook
---

# Playbook · AI 语音筛选（HackerRank Chakra 及同类）

> 通用打法，与公司无关。证据来自 `../../companies/snowflake/raw/chakra.md`（官方 KB / 打分博客 / release notes = high；聚合站 = medium）。公司特定剧本见各公司目录 `03-*-playbook.md`。
> 适用：Chakra（HackerRank）、以及任何「无真人、按 rubric 打分、追问自适应」的语音筛。

## 0. 这轮到底是什么

- **替代 recruiter 电话**：20–30 分钟，无真人，链接有有效期，不能排期、开始后不能暂停（唯一记载的暂停是违规触发）。
- **它是三个 agent**：Creator 把 JD 变成 sections + expectations；Interviewer 按计划追问、控时、跑题拉回；Reporter 事后**只读 transcript** 逐条 expectation 打分。
- **打分四档**：3 Met =「clarity, ownership, structured reasoning, specific examples 的具体证据」；2 Partially =「有相关证据但缺深度/具体性」；1 Not Met =「推理错误或只有 vague、theoretical 的回答」；0 Not Assessed =「transcript 里没有相关片段」。归一到 0–5 给 recruiter。
- **JD 上的 must-have 加权**。
- **人做最终决定**：recruiter 看 overall + 每 section 分 + 带时间戳的 transcript 引用 + 视频回放 + integrity flag。

## 1. 由打分机制直接推出的四条铁律

1. **没说到 = 0 分，不是中性。** 每个 section 至少把 rubric 的关键词（ownership / trade-off / 数字 / 工具名 / 验证方式）说出口一次。
2. **theoretical = Not Met。** 每个回答落到「我做过的一件事」，不讲原理课。
3. **只认 transcript。** 口误无所谓；被转错的**专有名词**会伤分 → 开 real-time transcript，看到转错就重述并拼读。
4. **追问是加分机会，不是否定。** 「escalating difficulty if responses are strong」；追问落在你刚才略过的那一段，所以首答留缝。

## 2. 回答形态：headline → mechanism → number → learning

```
headline   一句结论：我做了 X，结果 Y                       ~10 s
mechanism  怎么做的、为什么这样做、放弃了什么               ~40 s
number     可核验的量化（笔数 / 金额 / 行数 / 时间 / 比例）  ~10 s
learning   trade-off 或如果重来会改什么                    ~10 s
```

- 首答 **60–90 秒**（150–220 词），留 1–2 个追问空间；追问回答 30–60 秒。超过 2 分钟会被按时间切走，后半段可能不入 rubric。
- STAR 可用，但 Situation 压成一句——它不产生证据。
- 「I cut deploy time from 40 min to 12 by parallelizing the test stage」> 「I optimized the pipeline」。**说出真实的工具、真实的决定、真实的数字。**
- 每个故事准备两版：90 秒 + 追问版；追问方向固定四个：**你本人做了哪部分 / 为什么这个方案、弃了什么 / 结果数字、怎么验证 / 重来会怎么改**。

## 3. 20 分钟节奏（4 个 section 的典型配置）

| 时间 | 段 | 做什么 |
|---|---|---|
| 0–1 | 开场 | 它介绍议程。可以问它「how many sections, how long each」——它设计上会答议程类问题 |
| 1–6 | 经历 / 背景 | 自我介绍 60 s（定位一句 + 两个旗舰故事各一句 + 为什么这个岗位）；然后 1 个项目深挖 |
| 6–11 | 应用场景 | 岗位相关的「你会怎么做」——用**你做过的最接近的事**回答，再讲通用方法 |
| 11–16 | 协作 / 决策 | 一个跨团队故事 + 一个「我改了主意 / 我 pushback」故事 |
| 16–19 | 反问 | 问它**能答的**（next steps、这轮看重什么）+ 一句表态型（「下一轮我想和团队聊 X」）留在 transcript 里 |
| 19–20 | 收尾 | 一句总结：三个关键词 + 感谢 |

看到状态 **Thinking** 就闭嘴等；**Listening** 才开口。沉默无官方阈值，长停顿大概率被当作答完——用口头填充：「Let me think about that for a second — the key decision there was…」。

## 4. 操作清单（考前 30 分钟）

- [ ] **Chrome**，关掉其它 tab / 通知 / Slack / 任何 AI 或录屏扩展（截图分析会标 "browser extensions, external AI assistants"）
- [ ] **单显示器**（多显示器检测只在 Chrome 下做，检测到会暂停）；全屏不要退出
- [ ] 手机、平板移出画面（object detection 截图入报告）
- [ ] 有线耳机 + 麦克风；蓝牙延迟会让端点误判。预检时试麦、试扬声器、**打开 real-time transcript**
- [ ] 笔记本插电、稳定网络；断网无官方续考说明——真断了立刻回同一链接，同时邮件 recruiter
- [ ] 关键词卡贴在**摄像头旁边**（面不能长时间离开画面：「no face」会被逐次记录）；不要在屏幕上开第二个窗口
- [ ] 灯光在脸前、背景安静；摄像头全程开且录像，屏幕也可能被录

## 5. 面试中的应对

| 情况 | 做法 |
|---|---|
| 没听清 | 直接说 "Could you repeat the question?"（对话式 LLM，应能处理；未官方验证） |
| 名词被转错 | 下一句主动重述并拼读："to be precise, that's Kafka — K-A-F-K-A" |
| 被拉回主题 | 先答它问的，再用一句话带到你想讲的点；硬转话题「costs a turn」 |
| 它追问你略过的部分 | 这就是它的设计：给 mechanism + number，别重复 headline |
| 想不起数字 | 给量级 + 来源："on the order of 20 million transactions a year — that's from our 2025 impact summary" |
| 「questions for us」 | 它没有公司内部信息。问 next steps / 这轮权重；别问薪资、组、manager |
| 口音 / 非母语 | 语速放慢 10–20%，专有名词后跟一句解释；开 transcript 自查 |

## 6. 考后回写

- 记下**实际被问的每一道题**和追问，写进公司目录 `02-process.md` 的「亲历」节。
- 被追到答不上的部分 → 写回 `../stories/evidence-base.md` 对应故事。
- 这份 playbook 的「未验证」项（能否暂停、断网续考、能否让它重复、沉默阈值、是否打断、能否拿 transcript、是否有反问段）——亲历后逐条改成事实。
