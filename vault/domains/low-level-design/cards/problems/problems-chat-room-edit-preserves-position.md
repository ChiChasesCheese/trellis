---
id: problems-chat-room-edit-preserves-position
node: problems.social.chat-room
type: qa
step: 7
tags: [grown]
---
## Q
聊天室设计里，编辑一条已经发出的消息，为什么用 `dataclasses.replace` 生成新快照整体替换存储里的条目，而不是把 `Message` 设计成可变对象、直接改它的 `text` 字段？

## A
`Message` 是 `frozen=True` 的 `dataclass`——它被投递给多个在线成员、可能被多个调用方同时持有引用，冻结让它可以安全地在没有锁的情况下被共享和传递，不用担心某处代码意外改了别人手里那份引用看到的内容。编辑因此不能就地改字段，而是用 `dataclasses.replace(message, text=new_text, edited_at=now)` 生成一份新快照，再把存储里 `message_id -> Message` 这个字典条目整体替换成新快照。`seq` 和 `message_id` 在 `replace` 里不变，所以这条消息在历史列表里的相对位置完全不受影响——历史读到的永远是最新版本，但排序依据从未被编辑触碰过。这一步只改动 `MessageStore`，`ChatService.send_message` 的投递逻辑一行不用动。
