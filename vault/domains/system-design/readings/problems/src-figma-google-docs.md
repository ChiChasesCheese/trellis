---
nodes: [problems.media.google-docs]
url: https://www.figma.com/blog/how-figmas-multiplayer-technology-works/
tags: [engineering-blog]
---
# How Figma's multiplayer technology works

值得读：Figma 官方工程博客，记录了团队评估完整 CRDT 理论后认为大部分复杂度是为了满足"去
中心化环境"而 Figma 本来就有一个中心服务器，于是选择"属性级最后写入胜出（last-writer-
wins）+ 服务器校验树结构合法性"这一更简单的模型，并详述了如何用父链接属性和分数式排序
（fractional indexing）防止树结构产生环。本题解与它的分歧在于：Figma 的画布对象模型天然
是属性级的独立取值，但文本编辑的核心难点是"同一位置的并发字符插入"不能简单按属性取最后写
入胜出，这是本题解选择 OT 而不是 Figma 式简化 CRDT 的关键原因（详见题解「深入探讨」第 1
节）。
