---
id: streams-high-level-vs-transport-protocol-low-level
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
写网络代码时，什么情况下该用 `open_connection`/`StreamReader`/`StreamWriter` 这套高层 API，什么情况下才需要接触 `Transport`/`Protocol` 这套低层回调式 API？

## A
绝大多数应用代码应该只用高层 Streams API（`open_connection`、`start_server`），它把读写包装成可以直接 `await` 的接口，用起来符合 async/await 的直觉。`Transport`/`Protocol` 是基于回调（callback）风格的更底层接口，专为需要极致性能的库和框架实现（比如自己写一个高性能协议解析器）设计，官方明确建议普通应用代码不要直接使用它。
