---
id: problems-calendar-sync-token-invalidation
node: problems.realtime.calendar
type: qa
step: 7
tags: [grown]
---
## Q
A calendar client's incremental sync uses an opaque sync token to ask the server for changes since its last sync. CalDAV's sync-collection (RFC 6578) and the Google Calendar API handle an expired/invalid token differently at the protocol level — describe both, and state the principle they share.

## A
RFC 6578's sync-collection returns a `DAV:valid-sync-token` precondition failure when the server can no longer serve the requested token, requiring the client to restart with an empty token for a full resync. The Google Calendar API instead returns HTTP `410 Gone` in the same situation, requiring the client to clear its local store and perform a full resync. The protocols differ in mechanism but share the same principle: neither assumes the server can retain change history forever — both give the server an explicit way to tell the client 'your token is too old, start over' rather than silently returning an incomplete delta.

## Q zh
日历客户端的增量同步用一个不透明的 sync token 向服务端请求「自上次同步以来的变化」。CalDAV 的 sync-collection（RFC 6578）和 Google Calendar API 在协议层面对过期/失效令牌的处理方式不同——分别描述两者的做法，并说明它们共享的原则是什么。

## A zh
RFC 6578 的 sync-collection 在服务端无法再提供请求的令牌时，返回一个 `DAV:valid-sync-token` 前置条件失败，要求客户端用空令牌重新发起一次全量同步。Google Calendar API 在同样的情况下则返回 HTTP `410 Gone`，要求客户端清空本地状态并做全量同步。两种协议的具体机制不同，但共享同一个原则：都不假设服务端能永远保留完整的变更历史——两者都给服务端一个明确的方式告诉客户端「你的令牌太旧了、请重新开始」，而不是默默返回一份不完整的增量结果。
