---
id: hi-c-lld-rate-limiter-n14-sliding-log-allow
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 14
---
## Q
**限流器 · 滑动窗口日志的 allow**｜摘要 · 必会

滑动窗口日志的 `allow` 怎么写？重试时间怎么算？

## A
1. **取队列。**
2. **清理过期：** 截止点 `cutoff = now − windowMs`；只要队首时间戳早于截止点就出队，直到队首在窗口内或队列为空。先看队首（peek）再决定是否出队，比先出队再检查高效。
3. **判断：** 队列长度 < `maxRequests` 就放行：把 `now` 追加到队尾，`remaining = maxRequests − 追加后的长度`，重试时间为空。
4. **拒绝：** 最旧的那条是最先滑出窗口的。重试等待 = `最旧时间戳 + windowMs − now`，`remaining` 为 0。
- **例：** 最旧时间戳 50000，窗口 60000，现在 105000；它在 110000 滑出，要等 5000 毫秒。
- **边界约定：** 恰好等于截止点的时间戳算在窗口内还是外，要和重试时间公式保持一致，否则会差 1 毫秒（"等到时仍被拒"）。
