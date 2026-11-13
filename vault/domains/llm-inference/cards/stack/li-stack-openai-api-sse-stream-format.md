---
id: li-stack-openai-api-sse-stream-format
node: stack.openai-api
type: qa
step: 2
---
## Q
OpenAI 兼容接口的流式响应（SSE，server-sent events）具体长什么样？客户端怎么解析，测试要检查哪些细节？

## A
**SSE：** 一种基于普通 HTTP 响应的单向推送格式。响应头是 `Content-Type: text/event-stream`，响应体由一个个事件组成，每个事件是若干以 `data: ` 开头的行，事件之间用一个空行（`\n\n`）分隔。

**流式聊天的响应体示例：**

```text
data: {"id":"c1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"c1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"你好"},"finish_reason":null}]}

data: {"id":"c1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: {"id":"c1","object":"chat.completion.chunk","choices":[],"usage":{"prompt_tokens":12,"completion_tokens":3,"total_tokens":15}}

data: [DONE]
```

**规则：**
- 每块的 `object` 是 `"chat.completion.chunk"`，内容在 `delta` 里，是**增量**而不是全文。
- 第一块通常只带 `role`；最后一个内容块带 `finish_reason`。
- 请求了 `stream_options: {"include_usage": true}` 时，在结束前多一块，`choices` 为空数组，带 `usage`。
- 以 `data: [DONE]` 结束。

**测试要检查的细节：**
- **拼接等价：** 所有 `delta.content` 依次拼起来，必须等于同一请求非流式返回的 `content`（贪心解码下），`usage` 也必须一致。
- **多字节字符：** 一个汉字或 emoji 可能由多个 token 组成，任何一块都不能含有半个字符（表现为 `�` 替换符）。
- **结束完整：** 恰好一块带 `finish_reason`；有且只有一个 `[DONE]`；最后一块在 `[DONE]` 之前；`n > 1` 时每个 `index` 各自结束。
- **停止串：** 停止串不能部分泄漏，比如停止串是 `"###"`，流里不能先发出 `"##"` 再停。
- **心跳与超时：** 长时间排队时连接不应被中间代理因为空闲而断开。
- **错误中途发生：** HTTP 200 已发出后出错，状态码改不了，应该在流里发送一个带 `error` 的事件再关闭，客户端必须能识别。
