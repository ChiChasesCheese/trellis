---
id: bagu-db-consistency-4-double-delete
node: a.cache.db-consistency
type: qa
step: 4
---
## Q
**缓存一致性 · 延迟双删解决什么、缺什么**｜追问

面试官：「你提到先删缓存有并发问题，那延迟双删能解决吗？有什么缺陷？」

## A
**基本回答。** 延迟双删是：更新库之后先删一次缓存，等一段时间再删第二次，把中间被读请求写回的旧值清掉。等待的时间要大于「一次读库加写缓存」的耗时，比如 500ms。
**一句话记住。** 擦黑板擦了一遍，怕有人这时候翻旧账本又抄了上去，所以过一会儿再擦一遍，把这个「漏网的旧字」擦掉。擦的间隔太短，旧字还没抄上去就白擦了；太长，旧字挂着的时间就久。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<line x1="14" y1="52" x2="326" y2="52" stroke-width="1.2" stroke="currentColor"/>
<line x1="300" y1="52" x2="320" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="326.0,52.0 319.0,55.2 319.0,48.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="36" y1="46" x2="36" y2="58" stroke-width="1.2" stroke="currentColor"/>
<text x="36" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 删缓存</text>
<line x1="118" y1="46" x2="118" y2="58" stroke-width="1.2" stroke="currentColor"/>
<text x="118" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 更新库</text>
<line x1="204" y1="46" x2="204" y2="58" stroke-width="1.2" stroke="currentColor"/>
<text x="204" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B 写回旧值</text>
<line x1="296" y1="46" x2="296" y2="58" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 再删</text>
<text x="118" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">库已是新值</text>
<text x="204" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧值进缓存</text>
<text x="296" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">旧值被清掉</text>
<rect x="8" y="96" width="324" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="109.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">等待时间 > 一次读库加写缓存</text>
<text x="170" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">例如 500ms</text>
<text x="8" y="152" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">太短：旧值还没写回，清不掉</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">太长：不一致的时间更久，还占线程</text>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">所以做成异步：发一条延迟消息，到点再删</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">仍不是强一致，只是缩短旧值存活时间</text>
</svg>
时间轴从左到右：第一次删缓存，B 读库并写回旧值，库更新完成，等待一段时间后第二次删，旧值被清掉。下面是等待时间的设置依据和缺点。
**讲明白。**
- **解决什么问题：** 第一次删缓存之后、库更新完成之前，读请求可能读到旧值并把它写回缓存。第二次删就是把这个写回的旧值清掉。
- **它主要补的是「先删缓存」的坑：** 如果先删缓存、再更新库，这个并发窗口很大；双删让旧值最多只存活到第二次删。
- **等待时间怎么定：** 要大于一次「读库加写缓存」的耗时。先测读请求从读库到写回缓存的 P99（99% 的请求都在这个时间内完成），再加上余量，常见几百毫秒，比如 500ms。
- **缺点一：睡眠时间难估：** 太短，旧值还没被写回，第二次删就白做了，旧值留下来；太长，不一致的时间更久。
- **缺点二：占住线程：** 同步睡眠会占住请求线程，吞吐下降，线程池容易被占满。
- **所以通常做成异步：** 发一条延迟消息（MQ 延迟队列或延时任务），到点由消费者再删一次缓存，写请求不用等。消息要能重试，删失败才不会留旧值。
- **不能保证强一致：** 它只缩短不一致的窗口：第二次删之前，读到旧值的可能性仍在，睡眠时间估短了还清不掉。要更强的一致，要用订阅 binlog 删缓存并带重试，或给缓存加版本号。
**举个例子。** 榜单配置更新，读请求在 200ms 内会把旧值写回：
1. **时刻 0：** 更新库之前，先删一次缓存。
2. **时刻 50ms：** 另一个读请求未命中，去读库，此时库里还是旧值。
3. **时刻 100ms：** 库更新完成，榜单配置变成新值。
4. **时刻 200ms：** 读请求把旧值写回缓存，缓存里又是旧值。
5. **时刻 500ms：** 延迟消息触发，第二次删缓存，旧值被清掉。
6. **之后：** 下一次读未命中，回源读到新值，旧值只存活了半秒。
7. **睡眠估短的例子：** 如果只等了 100ms 就删，而读请求要 200ms 才写回，旧值就清不掉。
**容易错。**
- **以为双删等于强一致：** 它只缩短窗口，第二次删之前仍可能读到旧值。
- **睡眠时间随便写：** 要大于一次读库加写缓存的耗时，先测 P99 再加余量。
- **在请求线程里同步 sleep：** 会占住线程，要用延迟消息异步做。
- **延迟消息没有重试：** 删失败就留旧值，消息要能重试。
**业务场景。** 榜单配置更新后，读请求在 200ms 内写回旧值；延迟消息 500ms 后再删一次，旧值只存活半秒。
**系统设计。** [[links.tt-live-gift-coin-settlement|直播虚拟礼物：金币记账与主播结算]]：主播收入页缓存了汇总值，被问「账变更后缓存怎么不留旧值」，答延迟双删与它的缺点。
**可能问法。**
- 延迟双删的时间怎么定？ → 要大于一次读库加写缓存的耗时。先测读请求从读库到写回缓存的 P99，再加余量，常见几百毫秒，如 500ms。太短清不掉被写回的旧值，太长则不一致窗口更久。
- 为什么要异步？ → 同步睡眠会占住请求线程，吞吐下降，线程池容易被占满。改为发一条延迟消息（MQ 延迟队列或延时任务），到点由消费者再删一次缓存，写请求不用等。消息要能重试，删失败才不留旧值。
- 双删能保证强一致吗？ → 不能。它只缩短不一致窗口：第二次删除之前，读到旧值的可能性仍在，睡眠时间估短了还会清不掉。要更强的一致，要用订阅 binlog 删缓存并带重试，或给缓存加版本号。
