---
id: hi-sdx-ob-exemplars
node: more.observability
type: qa
step: 4
---
## Q
**示例点（exemplar）：从指标一步跳到追踪**｜补充 · 可观测性 · 加分

面试官：「面板上 p99 延迟突然飙高，你想立刻看到一个真正的慢请求。哪个特性可以从指标直接跳到追踪？它是怎么工作的？」

## A
**结论。** 示例点（exemplar）：往直方图桶里记录一次观测时，指标库顺手附上当前的追踪 ID。面板把它们画成延迟图上可点击的点，一点就进入属于慢桶的真实追踪。

**要点。**
- **机制：** 记录延迟观测时，同时附上当前请求的追踪 ID，作为这个桶的样本引用。
- **指标回答：** 哪里、多大程度变慢。
- **追踪回答：** 为什么慢。
- **示例点：** 把两者连起来，不必靠时间戳去另一个系统里翻。
- **前提：** 记录指标的地方要有活动的追踪上下文，OpenTelemetry 原生支持。

**为什么。** 指标是聚合，丢掉了单个请求的身份；示例点只保留少量代表请求的引用，成本很低，却补上了聚合到个例的缺口。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="60" y="8" width="220" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="24.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一次慢请求</text>
<text x="170" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">trace_id = 7f3a</text>
<polyline points="170,48 170,74" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,74 167.0,67.7 173.0,67.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="66" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">记录延迟 2.3 s</text>
<rect x="60" y="74" width="220" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直方图桶 le=5s</text>
<text x="170" y="107.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">附着示例点 7f3a</text>
<polyline points="170,118 170,144" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,144 167.0,137.7 173.0,137.7" style="fill:var(--accent,#3b6fd4)"/>
<rect x="60" y="144" width="220" height="40" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">延迟面板上的一个点</text>
<polyline points="170,184 170,210" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,210 167.0,203.7 173.0,203.7" style="fill:var(--accent,#3b6fd4)"/>
<text x="180" y="202" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">点击</text>
<rect x="60" y="210" width="220" height="40" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="234" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">打开 7f3a 的完整追踪</text>
</svg>

**面试里这样说。** 「p99 飙高时我在延迟面板上点桶里的示例点，直接打开那条慢请求的追踪，不用靠时间戳去追踪系统里猜。这要求指标记录处有追踪上下文，OpenTelemetry 默认支持。」

**易错。**
- **给每个指标加追踪 ID 标签：** 基数爆炸，示例点是样本引用，不是标签。
- **追踪被采样掉：** 示例点指向的追踪可能不存在，需要保证采样一致。
