---
id: bagu-why-protect-1-avalanche
node: b.protect.why-protect
type: qa
step: 1
---
## Q
**服务保护 · 雪崩怎么发生、五类手段**｜必会

面试官：「开票瞬间下游风控变慢，整条交易链路都挂了。一个慢依赖为什么能拖垮全部？该怎么防？」

## A
**基本回答。** 雪崩（cascading failure）：下游变慢（比直接挂了更糟，挂了立刻报错线程释放，慢则线程占着等超时、资源被悄悄耗光），上游线程池被占满，自己也不能响应，再上一层跟着被拖住，整条链路瘫痪；客户端每层重试 3 次，一个请求变成成倍请求砸在已很慢的下游。五类手段：限流（入口控制进来多少，保我不被调用方压垮）、熔断（对坏掉的依赖快速失败，保我不被被调用方拖垮）、降级（限流熔断后的兜底，关次要功能保核心）、隔离（资源分开，一个依赖变慢只耗自己那份）、超时加重试（每次调用有超时，重试有限次、带退避）。核心：让失败快速、局部发生，宁可拒绝一部分请求。
**2026 亮点。** 限流阈值写死会过时，更好是自适应：像 TCP 拥塞控制那样按延迟自动调并发上限（Vegas 或梯度控制），再按优先级丢弃；优先级和用户分组在入口打标并随调用链下传，各服务一致地丢同一批用户，避免每层各丢一点、整体成功率反而更低。取舍：实现和调参复杂，丢弃动作本身必须足够便宜。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 300">
<rect x="8" y="12" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">客户端（会重试）</text>
<rect x="8" y="62" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">网关</text>
<rect x="8" y="112" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">交易服务</text>
<rect x="8" y="162" width="140" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="183" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下游风控（变慢）</text>
<line x1="78" y1="46" x2="78" y2="55" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,62.0 74.8,55.0 81.2,55.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78" y1="96" x2="78" y2="105" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,112.0 74.8,105.0 81.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="78" y1="146" x2="78" y2="155" stroke-width="1.2" stroke="currentColor"/>
<polygon points="78.0,162.0 74.8,155.0 81.2,155.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="160" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 风控变慢，一个请求</text>
<text x="160" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">要等很久才返回</text>
<text x="160" y="124" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 线程都在等，线程池</text>
<text x="160" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被占满，无法响应</text>
<text x="160" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 网关的线程也被</text>
<text x="160" y="90" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拖住，层层蔓延</text>
<text x="160" y="24" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">④ 超时重试，流量</text>
<text x="160" y="40" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">被放大好几倍</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">五类手段：</text>
<rect x="8" y="232" width="62" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="39" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">限流</text>
<rect x="74" y="232" width="62" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">熔断</text>
<rect x="140" y="232" width="62" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="171" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">降级</text>
<rect x="206" y="232" width="62" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="237" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">隔离</text>
<rect x="272" y="232" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="302" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">超时重试</text>
<text x="8" y="284" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">核心：让失败快速、局部发生</text>
</svg>
从下往上读：①到④是故障蔓延顺序，最下一排是五类手段。
**业务场景。** 开票瞬间交易服务 20 个线程，风控平时 50ms，一线程每秒 20 个，池每秒 400；风控变成 5 秒后一线程每 5 秒处理 1 个，池每秒只有 4，每秒来 100 个请求，不到一秒线程全占住；网关跟着被占，客户端重试 3 次把 100 QPS 放大到约 300。有保护时超时 500ms、熔断打开后风控调用立刻失败走降级，线程马上释放。
**容易错。**
- **以为下游慢只影响下游。**
- **以为加机器就行：** 每台线程池照样被占满。
- **只做限流：** 下游变慢拖垮我的是出口方向，要靠熔断、超时、隔离。
