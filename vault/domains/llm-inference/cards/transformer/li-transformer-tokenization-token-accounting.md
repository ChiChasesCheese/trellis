---
id: li-transformer-tokenization-token-accounting
node: transformer.tokenization
type: qa
step: 2
---
## Q
接口返回的 `usage.prompt_tokens` 和 `completion_tokens` 是怎么算出来的？为什么用户自己数的 token 数常常和它对不上？怎样测试计数正确？

## A
**token：** 文字切成的小片段。计费、限流和上下文长度上限都按 token 计算。

**`prompt_tokens`（输入 token 数）包含的不只是用户的文字：**
- **对话模板的开销：** 消息列表要套上模型的对话模板（chat template）才变成模型输入，每条消息前后都有角色标记等特殊 token。一条"你好"可能在模板里变成十几个 token。
- **系统提示和工具定义：** 函数调用的 JSON 描述也被拼进模板，可能有上千个 token。
- **开始标记（BOS）：** 有些模型在开头加一个，有些不加。

**`completion_tokens`（输出 token 数）的口径：**
- 是否包括结束标记（EOS）；
- 遇到停止字符串时，被截掉的部分是否计入（模型已经生成了它们，算力已花掉）；
- "思考型"模型的推理过程 token 是否单独列出。

**用户对不上的常见原因：** 用了别的模型的分词器去数；只数了消息正文，没算模板；把字数当 token 数（中文 1 个字可能是 1–3 个 token）。

**测试方法：**
- **对照计算：** 用同一模型的分词器在测试代码里独立计算：`len(tok.apply_chat_template(messages, add_generation_prompt=True))`，应等于 `prompt_tokens`。
- **输出计数：** 开启 `logprobs` 后返回的 token 条数应与 `completion_tokens` 一致；`max_tokens=N` 且结束原因是 `length` 时，`completion_tokens` 应恰好等于 N。
- **流式与非流式一致：** 同一请求在 `stream=true`（并设 `stream_options: {"include_usage": true}`）和非流式下，`usage` 应完全相同。
- **边界：** 空字符串、只有系统提示、带图片输入（图片也会折算成 token）、请求被客户端中途取消时的计数。

计数错误直接变成计费错误，属于必须阻断发布的缺陷。
