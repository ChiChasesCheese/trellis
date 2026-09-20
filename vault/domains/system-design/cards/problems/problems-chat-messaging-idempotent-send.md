---
id: problems-chat-messaging-idempotent-send
node: problems.social.chat-messaging
type: qa
step: 5
tags: [grown]
---
## Q
In a chat system, a client's network retry after a timeout could otherwise cause the same message to be persisted and delivered twice. What mechanism prevents this, and what does the server do differently between a first send and a retried send?

## A
The client generates a `client_msg_id` (typically a UUID) once when the user hits send, and includes it on every retry of that same message. The server keeps a dedupe index keyed by (conversation_id, client_msg_id) with a TTL matching its offline-retention window. On the first send it persists the message and records the mapping to the resulting server-assigned message_id; on any retry with the same client_msg_id it does not persist or redeliver again — it just returns the original ACK (server message_id, sequence number, timestamp) it already produced.

## Q zh
在一个聊天系统中，客户端在超时后发起的网络重试原本可能导致同一条消息被持久化和投递两次。什么机制防止了这一点？服务器在首次发送和重试发送之间具体做了什么不同处理？

## A zh
客户端在用户点击发送时生成一个 `client_msg_id`（通常是 UUID），并在该消息的每次重试中携带同一个值。服务器维护一个按 (conversation_id, client_msg_id) 建索引的去重表，TTL 与离线保留窗口一致。首次发送时服务器持久化消息，并记录到最终生成的 server message_id 的映射；之后任何携带相同 client_msg_id 的重试都不会再次持久化或再次投递——只会返回它已经产生过的那个原始确认（server message_id、序号、时间戳）。
