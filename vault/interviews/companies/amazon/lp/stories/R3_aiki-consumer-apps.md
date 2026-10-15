# R3 · Aiki / AikiCard（个人消费者产品）

> 来源：**仅简历** Projects：Aiki（iOS，Mar 2024）、AikiCard（Web，Jun 2025）。没有故事笔记。
> 主 LP：**Customer Obsession**（仅在"用户可见产品"意义上）；副：Ownership · Learn and Be Curious · Invent and Simplify · Deliver Results。
> ⚠️ **薄**：只在被问 "customer" 且工作故事（S4/S9）已讲过一遍时作为第二个客户例子；不要让它成为 Customer Obsession 的主力。

## 1. 可用事实（简历原文）

| 事实 | 原文 |
|---|---|
| Aiki（iOS，Mar 2024） | 用 OpenAI 的 o3 做内容生成与自适应学习路径；本地存储 Core Data + CloudKit 同步；SwiftUI；StoreKit 内购；**4.5+ App Store 评分** |
| AikiCard（Web，Jun 2025） | React/Next.js/TypeScript；把 EPUB 书变成交互学习内容；Vercel edge 缓存全球加速；SM-2 间隔重复算法 + 进度追踪 + 自适应复习调度；TailwindCSS 响应式 UI |
| 缺 | 用户数、留存、反馈驱动的迭代、定价、你如何收集用户需求 |

## 2. 60–90 秒（口述提纲）

**"I built and shipped two learning products on my own; the iOS app holds a 4.5-plus App Store rating."**

**S · Situation**
- Two personal products: **Aiki**, an iOS flashcard app (**Mar 2024**), then **AikiCard**, a web platform (**Jun 2025**).
- Who the users are and what they told me: 【待 Chi 补：用户是谁、你听到的第一手用户反馈是什么】

**T · Task**
- I own **design, build, release and App Store review** on my own.

**A · Action** (in the order of the two projects)
1. **Aiki**: used OpenAI **o3** for content generation and adaptive learning paths.
2. **Aiki**: **Core Data** storage with **CloudKit** sync, **SwiftUI**, **StoreKit** purchases.
3. One thing I changed because of users: 【待 Chi 补：一个"用户说了某事 → 我改了产品"的具体例子，含数字（留存/评分变化/用户量）】
4. **AikiCard**: **React/Next.js/TypeScript** turns **EPUB books** into interactive study content.
5. **AikiCard**: **SM-2 spaced repetition** with progress tracking and adaptive review scheduling.
6. **AikiCard**: **Vercel edge caching** for fast global access.

**R · Result**
- **4.5+ App Store rating** on the iOS app.
- User numbers: 【待 Chi 补】

**L · Learning / Mechanism**
- 【待 Chi 补：从用户反馈里学到的规则/机制】

<details><summary>逐字稿（参考，不背）</summary>

> I built two learning products on my own, an iOS flashcard app and a web platform that turns EPUB books into interactive study material. The app has a 4.5-plus rating on the App Store. 【待 Chi 补：用户是谁、你听到的第一手用户反馈是什么】 One thing I changed because of users: 【待 Chi 补：一个"用户说了某事 → 我改了产品"的具体例子，含数字（留存/评分变化/用户量）】. On the web side I implemented SM-2 spaced repetition with adaptive review scheduling, and Vercel edge caching for fast global access.

</details>

## 3. 2 分钟（口述提纲）

等 Chi 补完 §2 的两个缺口后再成文：Situation（用户的痛）→ 你听到的证据 → 一个取舍（例如本地存储 + CloudKit 同步的取舍）→ 结果数字。

**"I built and shipped two learning products on my own; the iOS app holds a 4.5-plus App Store rating."**

**S · Situation**
- The user's pain: 【待 Chi 补】
- **Aiki** (iOS, Mar 2024), then **AikiCard** (web, Jun 2025).

**T · Task**
- Own **design, build, release and App Store review** alone.

**A · Action**
1. The evidence I heard from users: 【待 Chi 补】
2. A trade-off, for example **local storage plus CloudKit sync**: 【待 Chi 补】
3. **Aiki**: o3-driven content and adaptive paths, **Core Data + CloudKit**, **SwiftUI**, **StoreKit**.
4. **AikiCard**: **EPUB to interactive content**, **SM-2** with adaptive scheduling, **Vercel edge** caching.

**R · Result**
- **4.5+ App Store rating**; result numbers: 【待 Chi 补】

**L · Learning / Mechanism**
- What I'd do differently: 【待 Chi 补】

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Customer Obsession** (P) | 【待 Chi 补：用户反馈驱动的迭代】 | 4.5+ 评分背后的具体改动 | 无反馈就别说 obsession |
| **Ownership** (S) | "I own design, build, release and App Store review on my own." | 全栈、上架 | — |
| **Learn and Be Curious** (S) | "I learned SwiftUI, StoreKit and CloudKit to ship it." | 【待 Chi 补】 | — |
| **Invent and Simplify** (S) | "SM-2 plus adaptive scheduling so the learner doesn't decide what to review." | 间隔重复 | — |

## 5. 追问（≥5）

1. **Who are your users and how many?**
   - 【待 Chi 补】
2. **What's the most important thing a user told you?**
   - 【待 Chi 补】
3. **How does SM-2 work?**
   - 【待 Chi 补：用你自己的话讲 ease factor / interval 更新】
4. **CloudKit sync conflicts?**
   - 【待 Chi 补】
5. **How did you decide what to build first?**
   - 【待 Chi 补】
6. **Why o3 / how do you control LLM cost and quality?**
   - 【待 Chi 补】
7. **What would you change?**
   - 【待 Chi 补】

## 6. Senior 升级点（bar = senior）

当前档位：**无故事**。senior 级的 Customer Obsession 需要"用客户数据反推决策并且牺牲了某个短期目标"。若不能补出用户证据，**放弃本故事**，Customer Obsession 靠 S4 / S9 / S3，并按 `../question_bank.md` 的 fallback 回答。
