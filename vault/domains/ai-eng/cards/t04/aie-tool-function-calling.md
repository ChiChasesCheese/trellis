---
id: aie-tool-function-calling
node: t04.tool-design-agent-computer-interface
type: qa
step: 1
tags: [摘要]
---
## Q
**Tool design · function calling 的机制和"工具描述就是文档"**｜摘要 · 必会

模型怎么知道有哪些 tool、什么时候调用？你写的 tool 描述，对模型起什么作用？

## A
**机制（function calling）：** tool 就是一个函数，调用 tool 叫 function calling。大多数 API 的流程是：

1. **声明 tool inventory：** 每个 tool 给出入口（函数名）、参数、说明文档（它做什么、需要什么参数）。
2. **指定本次可用的 tool：** 常见的设置是 `required`（必须用至少一个）、`none`（不能用）、`auto`（模型自己决定）。
3. 模型输出"要调用哪个 tool、参数是什么"，你的代码执行它，把结果再交给模型。

```
# 模型的输出（示意）
tool_calls: [{ name: "lbs_to_kg", arguments: {"lbs": 40} }]
# 你的代码执行 lbs_to_kg(lbs=40)，用结果生成回答
```

**描述就是给模型的 API 文档：** 模型只看得到名字、参数和说明，所以它们决定模型会不会选对、填对。Anthropic 把这叫 agent-computer interface（ACI），建议投入和做人机界面差不多的精力：

- 描述写得像给新人看的 docstring，包含用法示例、边界情况、输入要求，以及和相近 tool 的区别；
- 测试：跑大量示例输入，看模型犯什么错，再改；
- **poka-yoke（防呆）：** 改参数让错误更难发生。例：模型离开根目录后用相对路径出错，改成**必须传绝对路径**就解决了；
- 格式贴近模型在互联网文本里常见的写法。

**出处：** Huyen《AI Engineering》ch6 §Planning → Function calling；Anthropic《Building effective agents》Appendix 2: Prompt engineering your tools
