# 01 · Recruiter 电话（30 min）

> 事实层在 `loop/LOOP_GUIDE.md` §1。题库在 `loop/rounds/01_recruiter/`。

## 这轮考什么

非技术 fit check：背景、why Stripe、职业目标、地点/签证、时间线。senior 岗可能由 HM 直接打；onsite 前还可能有第二次 30 分钟的 "informational call"。

评的是 **"clear, structured communication"**、相关经验、ownership / users-first 信号。

一句必须记住的话：

> **"cultural alignment is a hard filter, not a tiebreaker."**

不是加分项，是筛子。

## 有一条真实的红旗记录

2025-07 有候选人被 **recruiter 事后标了 red flag**，原因是他做了面试官**口头允许**的事（查语法、不必做完）。

结论：**一切以书面 prep 材料为准。** 面试官当场说的"没关系"，不代表评价体系认。这条对每一轮都适用。

## 必备的三个答案（背到能脱口而出）

**1. 30–60 秒经历概述**
不是简历朗读。结构：我是做什么的 → 最近做的一件有代表性的事 → 为什么这让我适合这个岗位。

**2. 具体的 why Stripe**
不能是"我喜欢支付"。必须包含：
- 对 **"increase the GDP of the internet"** 这句 mission 你自己的理解
- **点名一个**你用过或读过的 Stripe API / 工程博客

可用的具体素材（`loop/raw/stripe_official_and_api.md` §4）：Ledger 那篇（2024-02）、幂等 API 设计那篇（2017）、Paul Tarjan 的 rate limiter 那篇、Brandur 的 API versioning 那篇、Radar 那篇（2023）。**读过一篇，说得出一个观点，就够了。**

**3. why payments**
为什么是这个领域，不是"哪个大厂都行"。

## 不要做的事

| 不要 | 为什么 |
|---|---|
| 此阶段报薪资数字 | 说 "looking for a competitive offer"，先了解完整 package 再谈 |
| 提你在面的其他公司 | 这个阶段没有杠杆，只有风险 |
| 把 mission 说成套话 | "我认同你们的使命"= 什么都没说 |

## 时间线（心里有数，别追问 recruiter）

- 电面 → 结果：1–5 天
- 电面 → onsite：2–3 周（**可以主动要求延后**，这是正常请求）
- onsite → 决定：拒 2–5 天；5–10 工作日正常；**>2 周 = 进池等 team match / HC**
- 端到端 4–8 周；内推约 2 周；校招 9 月 OA → 12 月 onsite
- Cooldown：早期轮被拒 6 个月 / 推荐 12 个月

**recruiter ghost 和 headcount 撤回都有多例报道**，尤其校招受 returning intern 影响。心理上提前接受，别把它读成"我表现差"。

## 明天怎么练

```bash
python3 loop/mock.py bq recruiter -n 5
```

14 道题，抽了就**开口说**（录音）。重点练三个必备答案，每个说到 60 秒内不打磨。

## 自检清单

- [ ] 我的 60 秒自我介绍不是简历朗读
- [ ] 我的 why Stripe 里有一个具体的 API 或博客名字，且我真的读过
- [ ] 我能回答"why payments"而不是"why 大厂"
- [ ] 被问薪资我知道怎么绕开
- [ ] 我不会主动提在面的其他公司
- [ ] 我知道 recruiter 的口头允许**不代表**评价体系认

## 对应材料

- 题库：`loop/rounds/01_recruiter/{bank.json,questions.md,rubric.md}`
- 素材：`loop/raw/hr_hm_behavioral.md`、`loop/raw/stripe_official_and_api.md` §4（工程博客清单）
- 事实与来源：`loop/LOOP_GUIDE.md` §1
