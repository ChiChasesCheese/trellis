---
id: tc-illustrations
node: t02.illustrations-captions-focus-simplification
type: qa
step: 1
tags: [原则]
---
## Q
**Illustrations: captions, focus, simplification · 配图的写法**｜原则 · 追问

你要给文档加一张缓存架构图。图画好了，同事说："好看，但我不知道该看哪。" 按什么步骤做出一张能传递要点的图？

## A
**原则：** 先**写图注**，再画图；图要**聚焦**，每个元素按重要程度区分；**简化**到只剩一个要点；然后反复修改。

**怎么做：**
1. **先写图注：** 一句话，几个词，写出读者看完要记住什么。图是为它服务的。
2. **聚焦：** 在截图里用红圈、箭头标出重点，其余变淡；正文可以直接指着它说。
3. **简化：** 一张图的信息不超过一段话；系统复杂，就先画一张大图，再给每个子系统一张细图，或者逐步加细节。
4. **反复修改：** 问四个问题：怎么再简化？要不要拆成两张？文字够清晰吗？要点是什么？

**常见错法：**
- **图注是"图 3"：** 没有信息。
- **所有部分一样显眼。**
- **箭头来回不分：** 调用和返回用不同的线。

**示例：** Caption: "A cache hit skips the database." 图里只画 Client、Cache、DB 三个框，命中路径加粗，未命中路径变灰。

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing Two《Illustrating》（developers.google.com/tech-writing/two/illustrations：写图注、聚焦、简化、迭代）

</details>
