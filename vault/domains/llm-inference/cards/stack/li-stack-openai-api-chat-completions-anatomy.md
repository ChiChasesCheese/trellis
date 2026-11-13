---
id: li-stack-openai-api-chat-completions-anatomy
node: stack.openai-api
type: qa
step: 1
---
## Q
OpenAI 兼容的 `/v1/chat/completions` 接口有哪些关键请求参数和响应字段？每个字段的取值范围和含义是什么？

## A
**请求的关键参数：**
- **`model`：** 模型名，服务按它选择部署。
- **`messages`：** 消息列表，每条有 `role`（`system`、`user`、`assistant`、`tool`）和 `content`。服务端用对话模板把它们拼成模型训练时见过的文本格式。
- **`max_completion_tokens`（旧名 `max_tokens`）：** 最多生成多少个 token（token 是文字切成的小片段）。
- **`temperature`（0–2）、`top_p`（0–1）：** 控制从概率里选 token 的随机程度。`temperature=0` 近似总选概率最高的。
- **`stop`：** 停止字符串，OpenAI 的接口最多 4 个，生成内容中出现即停止，且不返回停止串本身。
- **`n`：** 为同一个输入生成几个独立回答。一些兼容实现只支持 1。
- **`seed`：** 随机种子，尽力保证可复现，不是严格保证。
- **`logprobs`、`top_logprobs`（0–20）：** 返回每个生成 token 的对数概率，以及每个位置概率最高的若干候选。
- **`stream`、`stream_options`：** 是否流式返回；`{"include_usage": true}` 让流的最后附带用量统计。
- **`response_format`：** 要求输出 JSON 或符合给定 JSON Schema。
- **`tools`、`tool_choice`：** 声明可调用的函数，模型可以返回函数调用请求。

**响应的关键字段：**
- **`id`、`object`（`"chat.completion"`）、`created`、`model`。**
- **`choices[i].message`：** 生成的 `content`，或 `tool_calls`。
- **`choices[i].finish_reason`：** `stop`（自然结束或遇到停止串）、`length`（达到长度上限）、`tool_calls`（模型要调用函数）、`content_filter`（被内容过滤截断）。
- **`usage`：** `prompt_tokens`（输入 token 数，包含模板开销）、`completion_tokens`（输出 token 数）、`total_tokens`。

**测试时最常出问题的组合：**
- `finish_reason` 与实际不符，例如达到长度上限却报 `stop`。
- 停止串被一并返回，或跨两个 token 时没被识别。
- `usage` 计数和用同一分词器独立计算的结果不一致。
- 不支持的参数（如 `n=2`）被静默忽略而不是报错。
