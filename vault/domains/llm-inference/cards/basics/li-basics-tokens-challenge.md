---
id: li-basics-tokens-challenge
node: basics.tokens
type: qa
step: 5
tags: [挑战]
---
## Q
**挑战。** 产品给输入框设了"最多 4,000 字"的限制，理由是模型窗口 8,192 token，"一个字一个 token，还剩一半留给回答"。上线后，一部分请求被服务端以超长拒绝，另一部分的回答写到一半就断了。哪里算错了？怎么改？

## A
**评分点（答出 3 条算过）：**

1. 窗口按 token 算，不按字数；换算不固定：常见汉字通常 1 个 token，生僻字、表情符号可以拆成 2–3 个，英文约 4 个字符 1 个 token。
2. 窗口由输入和输出共用，输入里还有用户看不见的部分：系统提示、对话模板的特殊 token、历史对话。
3. 最坏情况：4,000 个字每个 3 token 就是 12,000 token，直接超过窗口，被拒；勉强放进去时，留给输出的空间不够，回答写到上限被截断。
4. 改法：服务端用模型自己的分词器数 token，按"窗口 − 系统提示 − 历史 − 预留的输出"算出输入预算；前端的字数限制只当粗略提示。
5. 截断要看得见：检查停止原因是"到长度"还是"正常结束"，是前者就提示用户或续写。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 84" font-family="sans-serif" font-size="11">
<text x="160" y="14" text-anchor="middle" fill="currentColor">8,192 token 窗口：输入和输出共用</text>
<rect x="10" y="22" width="50" height="28" fill="currentColor" fill-opacity="0.15" stroke="currentColor"/>
<text x="35" y="40" text-anchor="middle" fill="currentColor">系统提示</text>
<rect x="60" y="22" width="30" height="28" fill="currentColor" fill-opacity="0.15" stroke="currentColor"/>
<text x="75" y="40" text-anchor="middle" fill="currentColor">模板</text>
<rect x="90" y="22" width="60" height="28" fill="currentColor" fill-opacity="0.15" stroke="currentColor"/>
<text x="120" y="40" text-anchor="middle" fill="currentColor">历史对话</text>
<rect x="150" y="22" width="100" height="28" fill="none" stroke="currentColor"/>
<text x="200" y="40" text-anchor="middle" fill="currentColor">用户输入</text>
<rect x="250" y="22" width="60" height="28" fill="currentColor" fill-opacity="0.3" stroke="currentColor"/>
<text x="280" y="40" text-anchor="middle" fill="currentColor">预留输出</text>
<line x1="150" y1="58" x2="250" y2="58" stroke="currentColor"/>
<line x1="150" y1="54" x2="150" y2="62" stroke="currentColor"/>
<line x1="250" y1="54" x2="250" y2="62" stroke="currentColor"/>
<text x="200" y="76" text-anchor="middle" fill="currentColor">输入预算：用分词器数 token</text>
</svg>

<details class="pt"><summary>参考答案</summary>错在把字数当成 token 数，并且忘了窗口是输入和输出共用的。常见汉字通常是 1 个 token，但生僻字和表情符号可能拆成 2 到 3 个，4,000 字最坏可以到 12,000 token，直接超窗口而被拒。输入里还有系统提示、对话模板的特殊 token 和历史对话，这些都占窗口，剩下的空间不够时回答就被截断。应该在服务端用模型自己的分词器计数，按窗口减去系统提示、历史和预留输出来算输入预算，并检查停止原因来发现截断。</details>
