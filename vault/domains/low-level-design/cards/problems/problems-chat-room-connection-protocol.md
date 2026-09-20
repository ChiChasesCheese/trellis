---
id: problems-chat-room-connection-protocol
node: problems.social.chat-room
type: qa
step: 4
tags: [grown]
---
## Q
聊天室设计里，“把消息投递给一个在线成员”这件事，用什么抽象表示？为什么用 `typing.Protocol` 而不是 `abc.ABC`？

## A
用一个只有一个方法的 `Connection`（`Protocol`）：`deliver(message: Message) -> None`。真实实现是一个包装 WebSocket 的适配器；测试里换成一个把收到的消息记进列表的假连接。选 `Protocol` 而不是 `abc.ABC` 的理由是结构化子类型（structural subtyping）：调用方只关心“这个对象有没有 `deliver` 方法”，被投递的一方不需要显式继承任何基类去声明“我是一个 Connection”，测试里的假连接因此可以是一个和真实实现毫无继承关系的普通类，只要方法签名对得上就能直接传进去。这是[[patterns.strategy|策略模式与可替换算法（Strategy）]]的标准形态：同一个动作有多种可替换的实现。
