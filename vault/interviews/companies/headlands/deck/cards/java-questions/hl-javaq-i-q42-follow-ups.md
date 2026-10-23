---
id: hl-javaq-i-q42-follow-ups
node: java-questions.i-network
type: qa
step: 10
---
## Q
追问：为什么看分位数而不是平均？为什么测间隔用 `System.nanoTime` 而不是 `currentTimeMillis`？
Why measure percentiles instead of averages?

## A
- **分位数**：尾延迟决定交易结果；平均会掩盖尖刺。
- **`nanoTime`**：单调、高分辨率；`currentTimeMillis` 会随系统时钟调整。
- 每次改动后重新测，不靠经验口诀。
