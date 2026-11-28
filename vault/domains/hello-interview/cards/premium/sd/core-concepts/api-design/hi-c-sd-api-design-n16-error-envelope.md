---
id: hi-c-sd-api-design-n16-error-envelope
node: sd.core-concepts.api-design.notes
type: qa
step: 16
---
## Q
**API 设计 · 统一错误响应**｜摘要 · 追问
状态码已经表示出错了，响应体里还要放什么？为什么形状要全站统一？

## A
- **分工：** 状态码说"哪一类问题"，响应体说"具体是什么问题"。
- **信封（envelope）：** 每个端点的错误都长一样，如 `{"error": {"code": "SEAT_UNAVAILABLE", "message": "VIP 区只剩 1 个座位"}}`。
- **code 与 message 的区别：** code 是稳定字符串，客户端代码按它分支（看到 `SEAT_UNAVAILABLE` 就弹选座界面）；message 给人看，随时可改而不会破坏任何人。
- **统一形状：** 调用方只需写一次错误处理。面试里一句"错误返回统一信封，带机器可读错误码"就够。
