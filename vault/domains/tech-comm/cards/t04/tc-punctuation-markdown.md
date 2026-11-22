---
id: tc-punctuation-markdown
node: t04.punctuation-markdown
type: qa
step: 1
tags: [原则]
---
## Q
**Punctuation & Markdown · 标点与格式**｜原则 · 追问

你的文档里有一句："The service retries, it uses exponential backoff, however it gives up after five tries" 评审人圈出了逗号。还有个同事问："用 Markdown 写技术文档要注意什么？"

## A
**原则：** 标点是**停顿的标记**，用来让读者的呼吸和你的意思对上。Markdown 是文档的轻量格式。

**标点硬规则：**
| 标点 | 用法 |
|---|---|
| 逗号 | 读者自然停顿处；分隔并列项（建议用最后的逗号）；条件和结果之间；成对的逗号圈出补充 |
| Comma splice | 两个独立的句子只用逗号接起来是错的，改成句号 |
| 分号 | 连接两个**关系紧密且各自完整**的句子；后面接 however、therefore 时，其后加逗号 |
| 破折号 | 比逗号更长的停顿 |
| 括号 | 少用，只放次要的话 |

**Markdown 惯例：** `##` 标题；`**粗体**`、`*斜体*`；`*` 或 `-` 开头的列表；缩进四个空格显示原样代码；`> [!NOTE]` 做提示块。

**改写示例：**
- Before: "The service retries, it uses exponential backoff, however it gives up after five tries."
- After: "The service retries with exponential backoff; however, it gives up after five tries."

**常见错法：**
- **用逗号拼接两句话。**
- **用分号做列表分隔：** 并列项里用逗号。
- **过多括号和破折号。**

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing One《Punctuation》（developers.google.com/tech-writing/one/punctuation）；《Markdown》（developers.google.com/tech-writing/one/markdown）

</details>
