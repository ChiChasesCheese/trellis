---
id: tc-slides-storyboards
node: t02.slides-storyboards
type: qa
step: 1
tags: [原则]
---
## Q
**Slides & storyboards · 幻灯片**｜原则 · 追问

你要为 design review 做六页幻灯片。你的第一版：每页标题是"背景""方案""风险"，正文是满满的要点。评审人看了看说："所以你想让我们决定什么？" 怎么改？

## A
**原则：** 幻灯片是金字塔的**视觉版本**：每页标题是一句**完整的结论**，页面内容用来证明这句话；全套幻灯片的标题连起来读，就是你的论证（storyboard）。

**怎么做：**
1. 先写 storyboard：每页一句话标题，按论证顺序排好，连起来读通顺。
2. 文字页：标题写结论，正文放它下面的要点，要点概括同组内容。
3. 图表页：标题写图要说明的结论，图只留支持它的数据，其余去掉。
4. 第一页给 SCQA 或结论；最后一页写要对方做的决定。
5. 每页只证明一件事。

**常见错法：**
- **主题式标题（"背景""风险"）：** 读标题得不到论证。
- **一页塞多个图：** 看不出哪个重要。
- **图表没有结论标题：** 观众自己去解读。

**改写示例：**
- Before: Title: "Cache performance". Body: a chart and six bullets.
- After: Title: "Redis cut p99 latency from 400 ms to 90 ms". Body: one chart, one takeaway.

**出处：** Minto p. 209–224（Ch.11 Reflecting the Pyramid on a Screen：Designing Text Slides / Designing Exhibit Slides / Story Boarding）
