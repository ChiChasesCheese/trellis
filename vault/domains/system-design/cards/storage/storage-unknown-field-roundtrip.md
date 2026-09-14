---
id: storage-unknown-field-roundtrip
node: storage.encoding
type: qa
---
## Q
During a rolling upgrade, new code adds a `nickname` field to user records. Users set nicknames — then some mysteriously revert to empty, with no errors logged anywhere. Reconstruct the bug.

## A
An **unknown-field round-trip loss**, done by *old* code that was individually forward-compatible:

1. New code writes a record including `nickname`.
2. An old instance **reads** it — its decoder tolerantly skips the unknown field (forward compatible, no error).
3. The old instance decodes into its model object (which has no `nickname` slot), modifies something, and **writes the whole record back**. The unknown field, never captured, is silently gone.

The lesson: forward compatibility on *read* is not enough — any **read-modify-write** path must **preserve fields it doesn't understand** through the round trip. Some codecs retain unknown fields in the decoded object (Protobuf reattaches unknown tags on re-serialize); ORMs and hand-rolled model classes are the classic offenders, dropping anything not in the mapping. It's insidious precisely because nothing fails — data just quietly evaporates until someone notices.

## Q zh
滚动升级期间，新代码给用户记录加了 `nickname` 字段。用户设置了昵称 — 然后一部分昵称神秘地变回空，任何地方都没有报错日志。还原这个 bug。

## A zh
一次**未知字段的 round-trip 丢失**，肇事者是各自都做到 forward 兼容的*旧*代码：

1. 新代码写入一条包含 `nickname` 的记录。
2. 一个旧实例**读取**它 — 它的解码器宽容地跳过这个不认识的字段（forward 兼容，无报错）。
3. 旧实例解码到自己的模型对象里（那里没有 `nickname` 这个槽位），修改了别的东西，然后**把整条记录写回**。从未被捕获的未知字段就这样无声地消失了。

教训：*读取*时的 forward 兼容还不够 — 任何**读-改-写**路径都必须让不理解的字段**穿过整个 round trip 被保留下来**。有些编解码器会在解码对象里保留未知字段（Protobuf 重新序列化时会带回未知 tag）；ORM 和手写的模型类是经典肇事者，凡是不在映射里的都被丢掉。它的阴险恰恰在于什么都没失败 — 数据只是安静地蒸发，直到有人注意到。
