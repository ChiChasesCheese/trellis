# 08 · Behavioral / 最终 HM（30–45 min）

> 事实层在 `loop/LOOP_GUIDE.md` §8。题库在 `loop/rounds/08_behavioral/`。

## 先说一件事：这轮的投入产出比最高

编程轮的撞题率是 30–55%，**行为轮是 100% 可准备、0% 靠运气**。同样两小时，花在这里的确定性回报最高。

而且它能一票否决你：Hiring Committee 写 1–4 分书面反馈，**"一个 lukewarm 即拒"**。有 L3 全 hire、仅一轮 lean-no 被 C-level 否掉的案例；也有 L4 因为**"behavioral 里用了技术术语"**被拒的案例。

## 形式

社招是 onsite 里的一轮，校招 = HM chat（见 `02-hm.md`）。但注意：**"behavioral woven into every round"** —— 每一轮的闲聊都在评。

## STAR-L 模板（比 STAR 多一个 L）

| 段 | 长度 | 要点 |
|---|---|---|
| **S** ituation | 1–2 句 | 别铺垫背景，直接进冲突 |
| **T** ask | 1 句 | **用 "I" 不用 "we"** —— 这条被反复点名 |
| **A** ction | **≥50% 篇幅** | 3–5 个动作，**必须包含 alternatives → 为什么选这个** |
| **R** esult | 1–2 句 | **量化**，并且**回到用户** |
| **L** earning | 1 句 | 今天会怎么做 + 这个教训后来用在哪 |

**Action 占一半以上**，这是最多人做错的比例 —— 大多数人把时间花在 Situation 上。

**没有 alternatives 的故事等于没有决策**，而他们要看的就是你怎么决策。

## 六个故事，两个版本

准备 **6 个故事 × 90 秒版 / 3 分钟版**，覆盖：

**ownership · 冲突 · 失败 · 模糊或紧迫 · 质量 · 学习**

为什么要两个版本：HM 会打断。有一手反馈说面试官 "kept interrupting"，候选人被打断后接不上就崩了。**90 秒版就是被打断后的重启点。**

模板和覆盖矩阵在 `loop/rounds/08_behavioral/stories.md` —— 它给的是骨架和自检问题，**不替你编经历**。

## Operating Principles 覆盖矩阵

Stripe 按自己的 Operating Principles 打分：

Users first · Move with urgency and focus · Be meticulous / craft · Seek feedback / collaborate egolessly · Deliver outstanding results · Stay curious · Obsess over talent · Macro-optimistic / Resilient · Humble · Rigorous thinking

**做法**：把 6 个故事横着排，10 条原则竖着排，自己打勾。**没被任何故事覆盖的原则，就是你的洞。**
矩阵在 `stories.md`；每条原则"面试官在找什么 / 故事必须含什么 / 反例"在 `loop/raw/hr_hm_behavioral.md`。

（官方原则文案 2026-09 复核过，无变化。）

## 挂点 → 对策

| 挂点 | 对策 |
|---|---|
| 故事太长，被打断后接不上 | 练 90 秒版 |
| 只讲技术、不讲用户结果 | 每个 Result 都要落到用户或业务数字上 |
| 没有 alternatives / trade-off | Action 里必须有"我当时还考虑过 B，没选是因为……" |
| 把分歧对方说成傻子 | 说出**对方的理由为什么合理**，再说你为什么仍然选了另一条 |
| 术语堆砌 | 有 L4 因此被拒。**讲给非技术的人听** |
| 全程 "we" | 面试官分不清你做了什么。Task 和 Action 用 "I" |

## 明天怎么练（具体到命令）

```bash
python3 loop/mock.py bq behavioral -n 5 -m 3    # 随机抽 5 题，每题限时 3 分钟
python3 loop/mock.py bq hm -n 3
```

练法：

1. 抽题 → **计时开口说**（录音）
2. 回放，用 `loop/rounds/08_behavioral/rubric.md` 自评
3. 重点听三件事：Action 占了几成？有没有 alternatives？Result 落到用户没有？

题库 50 题（其中 28 条是 Stripe 一手原题，另外 22 条是跨公司迁移练习，source 字段里标明了）。

**别只在心里过。** 心里想的和嘴里说出来的差距，只有录音能告诉你。

## Stripe 专属高频题

- 从头到尾 own 一件事
- 不是你的责任但你顶上了
- 信息不全时怎么决策
- 一切都紧急时怎么排序
- 一个复杂的技术决策
- 你改变主意的一次
- 与工程师 / 经理的分歧
- 一次失败
- 你对高质量的标准
- 收到负面反馈
- 技术债
- mission 对你意味着什么

最后一条要具体：**点名一个你用过或读过的 Stripe API / 工程博客**，别说套话。

## 自检清单

- [ ] 我有 6 个故事，每个都有 90 秒和 3 分钟两个版本
- [ ] 每个故事的 Action 占一半以上篇幅
- [ ] 每个故事都有"我还考虑过 B，没选是因为……"
- [ ] 每个 Result 都有数字，且回到用户
- [ ] 10 条原则的覆盖矩阵我打过勾，洞补上了
- [ ] 我录音听过至少 3 个故事
- [ ] 我的 why Stripe 里有一个具体的 API 或博客名字
- [ ] 我讲分歧时能说清对方为什么也有道理

## 对应材料

- 题库：`loop/rounds/08_behavioral/{bank.json,questions.md,stories.md,rubric.md}`
- 原则映射：`loop/raw/hr_hm_behavioral.md`
- 事实与来源：`loop/LOOP_GUIDE.md` §8
