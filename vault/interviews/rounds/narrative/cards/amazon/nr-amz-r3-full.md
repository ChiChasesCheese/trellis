---
id: nr-amz-r3-full
node: amazon.full
type: qa
step: 15
---
## Q
<p class="title">Aiki 消费者 App<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我独自做了两个学习类产品，2024-03 的 iOS 闪卡 app Aiki，和 2025-06 的 Web 平台 AikiCard，后者把 EPUB 书变成交互式学习内容。
- 我的角色：设计、开发、发布和 App Store 审核都由我一个人负责，所以每个环节的好坏都归我。
- Aiki 怎么做：用 OpenAI o3 生成内容和自适应学习路径，用 Core Data 加 CloudKit 做存储和同步，SwiftUI 做界面，StoreKit 做内购。
- AikiCard 怎么做：用 React、Next.js、TypeScript，实现 SM-2 间隔重复、进度追踪和自适应复习调度，学习者不用自己决定复习什么；Vercel edge 缓存让全球访问更快。
- 结果：iOS app 在 App Store 保持 4.5 以上评分；用户数和具体的反馈驱动改动我没有记录，所以只讲产品本身。

<span class="label">英文口述（60–90 秒）</span>

I built two learning products on my own: Aiki, an iOS flashcard app from March 2024, and AikiCard, a web platform from June 2025 that turns EPUB books into interactive study material. I owned design, development, release and App Store review. On the iOS side I used OpenAI o3 for content generation and adaptive learning paths, Core Data with CloudKit for storage and sync, SwiftUI for the interface, and StoreKit for in-app purchases. On the web side I implemented SM-2 spaced repetition with progress tracking and adaptive review scheduling, so learners don't have to decide what to review, and Vercel edge caching for fast global access. The iOS app holds a 4.5-plus rating on the App Store.

<div class="sources"><b>表达 · business English</b><br>• <b><i>own it end to end</i></b> — 从头到尾全权负责<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I owned both products end to end, from design to App Store review.”</span><br>• <b><i>ship to production</i></b> — 真正发布上线<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I shipped the iOS app through App Store review on my own.”</span><br>• <b><i>adaptive scheduling</i></b> — 自适应调度（按学习情况安排复习）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Adaptive scheduling means the learner doesn&#x27;t have to decide what to review.”</span></div>
