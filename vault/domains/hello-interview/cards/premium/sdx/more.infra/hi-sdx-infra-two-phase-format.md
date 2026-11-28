---
id: hi-sdx-infra-two-phase-format
node: more.infra
type: qa
step: 3
---
## Q
**改数据格式分两次发布**｜补充 · 平台基础设施：容器、服务网格、发布 · 追问

面试官：「要改一个持久化或线上传输的数据格式，怎么发布才安全？」

## A
**结论。** 把改动拆成两次发布，这是扩展再收缩在部署时序上的孪生做法。发布 1「准备」：代码能读新格式，但仍写旧格式，先在所有实例上铺开。发布 2「激活」：开始写新格式，最好放在功能开关后面，激活变成运行时开关而不是一次发布。口诀：读者先于写者。

**要点。**
- **任何时刻都成立：** 滚动到一半、发布 2 回滚之后，每个在跑的版本都能读懂任何版本写下的数据。
- **开关的作用：** 激活不再需要发布，出问题关开关就能退回旧格式，已写下的新格式数据仍能被读懂。
- **一步发布的坏处：** 新旧版本并存的窗口里，旧实例读到新格式就崩，或者悄悄丢字段。
- **收缩：** 确认没有实例再写旧格式，才在以后的发布里删除旧格式的读取代码。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 254">
<rect x="8" y="10" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170.0" y="28.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发布 1「准备」：能读新格式，仍写旧格式</text>
<text x="170.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">全部实例铺开之后，才允许下一步</text>
<polyline points="170,54 170.0,73.0" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170,80 166.8,73.0 173.2,73.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="8" y="80" width="324" height="44" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">发布 2「激活」：开始写新格式</text>
<text x="170.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最好放在功能开关后面，变成运行时开关</text>
<line x1="8" y1="144" x2="332" y2="144" stroke-width="1" stroke="currentColor" opacity="0.4" stroke-dasharray="3 3"/>
<text x="8" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">铁律：先能读，后写（读者先于写者）</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">任何时刻（包括滚动到一半、回滚发布 2 之后），</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">所有在跑的版本都能读懂任何版本写下的数据</text>
<text x="8" y="238" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一步发布 = 新旧版本并存的窗口里必有读不懂的数据</text>
</svg>

**面试里这样说。** 「改格式我分两次发布：第一次只加读取新格式的能力，铺满之后第二次才开始写，激活放在功能开关后面。任何时刻新旧版本都能读懂对方写的东西。」

**易错。**
- **先发写者：** 读者还没升级，新格式的数据一出现就读不了。
- **激活后立即删旧格式的读取：** 回滚或晚到的旧数据会读不出来。
