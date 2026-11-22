---
id: tc-standups
node: t05.standups-weekly-updates
type: qa
step: 1
tags: [原则]
---
## Q
**Standups & weekly updates · 站会与周报**｜原则 · 追问

站会每人轮流说一遍："昨天我做了 A、B、C，今天做 D。" 十五分钟后没人记得谁卡住了。周报也一样，经理问："所以进度如何？" 怎么改？

## A
**原则：** 更新的重点是**状态与阻碍**，不是活动清单。先说结论（on track / at risk / blocked），再说关键进展，最后说你需要什么。

**怎么做：**
1. 开头一个词：状态（On track / At risk / Blocked）。
2. 进展：一两条，按结果写（"checkout migration is 80 percent done"），不写过程。
3. 阻碍：说清楚卡在哪、需要谁做什么、什么时候之前。
4. 周报用固定模板，每周同样的栏目，读者很快扫完。
5. 变化在前：和上周相比变了什么。

**常见错法：**
- **罗列活动：** "开了会，看了代码。" 读不出进展。
- **阻碍藏在中间。**
- **每次格式不同。**

**改写示例：**
- Before: "Yesterday I looked into the retry bug and talked to Sam and read some logs."
- After: "At risk: the retry fix. Root cause found; the fix needs a schema change. I need Sam's review by Wednesday to stay on schedule."

**出处：** Orosz《The Software Engineer's Guidebook》ch16 §5 Day-to-Day Project Management（部分）；句式由规则推导
