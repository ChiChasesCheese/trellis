---
id: hl-ld01-pad-deadlock
node: problems.ld01-spsc-channel
type: qa
step: 9
---
## Q
变长消息回绕时为什么需要 PAD 记录？为什么 PAD 必须单独发布，否则会怎样死锁？

## A
数据区是环，但**一条记录必须连续**。当前位置到末尾放不下整条记录时：先在当前位置写一条 **PAD 记录**（`len = -1`）占满到数据区末尾，再从偏移 0 开始写真记录。消费者读到 `len == -1` 就知道「这一段是填充，直接跳到开头」。例：`capacity=64`，tail 在 48，要写 24 字节记录，到末尾只剩 16：写 16 字节 PAD，再从 0 写 24 字节，`bytesPending() == 40`。

**错的第一版**：`if (pad + rec > 空闲字节) return false; 写 PAD；写记录；发布 tail`——整体判断。**会死锁**：环是空的（`head == tail`），但 `tail` 恰停在偏移 8（`toEnd = 56`），生产者想发 `maxPayload` 的大消息（记录 64 字节）：需要 PAD 56 + 记录 64 = 120 > 64 → 永远 `false`；消费者没东西可读，`head` 不前进，空间永不增。双方互等：**活性丧失**。

**修复：PAD 单独发布**。需要 PAD 时只要有 `toEnd` 字节空位就写 PAD、`tail += toEnd`、release 发布，哪怕随后真记录挤不进（`offer` 返回 `false`）。消费者 `poll` 读到 PAD 跳到开头并**立即发布 head**，环重新「空且 tail 在偏移 0」，任何 ≤ `maxPayload` 的消息都放得进。

```java
if (rec > toEnd) {                             // 放不下连续的一整条
    if (!hasRoom(t, toEnd)) return false;
    seg.set(JAVA_INT_UNALIGNED, HEADER_BYTES + idx, PAD);
    t += toEnd; tail = t;
    LONG.setRelease(seg, OFF_TAIL, t);         // PAD 先发布
    idx = 0;
}
if (!hasRoom(t, rec)) return false;            // 之后真记录放不下 return false，PAD 已发布
```
**代价**：`offer` 返回 `false` 时 `tail` 可能已变（对消息序列无影响，但 `bytesPending` 含 PAD）。

正确的活性性质是 **`offer → poll → offer`**，要求两边同时做对：生产者单独发布 PAD，消费者越过 PAD（`poll` 返回 `null`）。「空环上连续两次 `offer` 就放得进」是错的——PAD 占的字节要等消费者越过才释放。

**练习**：容量 64、`head = tail = 8`，发 60 字节（记录 64）：第一次 `offer` 写 PAD（56 字节）并发布 `tail=64`，但空位只有 8 放不下真记录 → `false`，`bytesPending()=56`；`poll` 跳过 PAD，`head=64`，返回 `null`，`bytesPending()=0`；第二次 `offer`：`idx=0`，不需 PAD，空位 64 ≥ 64 → `true`，`bytesPending()=64`。
