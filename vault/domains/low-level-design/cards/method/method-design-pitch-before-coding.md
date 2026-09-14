---
id: method-design-pitch-before-coding
node: method.delivery
type: qa
---
## Q
You have a class sketch and 60 minutes of coding ahead. How do you present the design in ~3 minutes so the interviewer can redirect you *before* you write code?

## A
Present it as a **walk, not a catalogue**:

- Name the 5–7 core types in one breath, then trace one flow through them: "`Gate` asks `SpotAllocator` → `Lot` reserves → `Ticket` issued."
- Call out the **variation points** you're putting behind interfaces and why (`FareStrategy`, because pricing was hinted at).
- State what you're deliberately leaving as a stub, then explicitly ask: "anything you want moved before I start typing?"

The ask is the point — a redirect costs 30 seconds now and 20 minutes after the code exists.


## Q zh
你有一个类草图和 60 分钟的编码。你怎样用约 3 分钟展示设计，让面试官能在你写代码**之前**重定向你?

## A zh
以**行走而不是目录**的形式展示:

- 一口气命名 5–7 个核心类型，然后追踪一个流经过它们:"Gate` 问 `SpotAllocator` → `Lot` 预留 → `Ticket` 发出。"
- 指出**变化点**你在接口后面放置以及为什么（`FareStrategy`，因为定价被暗示了）。
- 说明你有意留作存根的内容，然后明确问："你想在我开始输入之前移动什么吗?"

这个问题很关键 — 一个重定向现在花 30 秒，代码存在后花 20 分钟。
