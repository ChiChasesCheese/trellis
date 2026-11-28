---
id: bagu-cap-base-4-per-business
node: a.distributed.cap-base
type: qa
step: 4
---
## Q
**按业务取舍 · 支付、评论、点赞各选什么**｜必会

面试官：「支付、评论、点赞三个业务，你分别选一致还是可用？」

## A
**基本回答。** 按出错的代价选，而且按操作取舍，不是按系统整体。支付扣款选一致：宁可拒绝服务、让用户稍后重试，也不能多扣少扣；余额展示可以选可用，返回稍旧的值并标注。评论选可用加最终一致：发评论先写成功，本人立即能看到，别人晚几秒可见。点赞选可用：计数短暂不准可以接受，异步落库，最终一致。
**一句话记住。** 问自己一句话：「这里出错了，是要赔钱，还是只让人多等几秒或看到旧数字？」赔钱的选一致，其他的选可用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个系统里，按操作分别取舍</text>
<rect x="8" y="24" width="92" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="54" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">扣款</text>
<line x1="100" y1="41" x2="105.0" y2="41.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="112,41 105.0,44.2 105.0,37.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="112" y="24" width="220" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="222" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选一致：宁可拒绝，不多扣少扣</text>
<rect x="8" y="66" width="92" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">余额展示</text>
<line x1="100" y1="83" x2="105.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="112,83 105.0,86.2 105.0,79.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="112" y="66" width="220" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="87" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选可用：返回稍旧的值并标注</text>
<rect x="8" y="108" width="92" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">评论</text>
<line x1="100" y1="125" x2="105.0" y2="125.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="112,125 105.0,128.2 105.0,121.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="112" y="108" width="220" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可用 + 最终一致：本人立即可见</text>
<rect x="8" y="150" width="92" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="54" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">点赞</text>
<line x1="100" y1="167" x2="105.0" y2="167.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="112,167 105.0,170.2 105.0,163.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="112" y="150" width="220" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="222" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">选可用：计数不准几个没关系</text>
<text x="8" y="206" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">判断标准：哪个代价小就选哪个</text>
</svg>
四个业务对应四个选择，只有涉及钱的扣款是「宁可不可用也要一致」。
**讲明白。**
- **取舍的依据：** 一致性的代价是变慢或不可用，可用性的代价是短暂的错误数据。哪个代价小，就选哪个。
- **按操作取舍：** 同一个支付系统里，扣款是资金变动，选一致；余额展示只是看一眼，选可用即可。不要给整个系统贴一个标签。
- **支付扣款：** 宁可拒绝服务、让用户稍后重试，也不能多扣少扣，因为多扣少扣是真金白银的损失，还要走退款和对账。
- **余额展示：** 返回稍旧的值并标注「以实际为准」，用户能接受，也不会引起资金风险。
- **评论：** 发评论先写成功，本人立即能看到，别人晚几秒可见。选可用加最终一致，换来高吞吐。
- **读己所写（本人立即可见）：** 评论的「本人立即可见」叫读己所写（read-your-writes）：写后的读取走主库或本地缓存，别人读副本。
- **点赞：** 点赞数短暂差几个，用户几乎感知不到，也没有资金损失；强一致要同步协调，代价是变慢甚至不可用。所以异步落库，计数最终一致。
- **常见组合：** 同一个系统内，写路径选一致、读路径选可用。
**举个例子。** 用户发一条评论：
1. **写入成功：** 评论写入主库，立刻返回成功。
2. **作者自己刷新：** 读主库或本地缓存，马上看到自己的评论（读己所写）。
3. **其他观众：** 读的是副本，副本还没同步到，几秒内看不到。
4. **副本追上以后：** 所有人都能看到，达到最终一致。
对比扣款：用户 A 余额 100，扣 100 时若遇到分区，系统宁可返回「请稍后重试」，也不会让同一笔 100 在两边各扣一次。
**容易错。**
- **以为整个系统选一个 CP 或 AP：** 要按操作分别选，扣款和余额展示在同一个支付系统里取舍就不同。
- **以为点赞也要强一致：** 点赞不涉及资金，强一致只会拖慢、拖垮可用性。
- **以为选可用就是不管对不对：** 选可用要配套最终一致、异步落库和对账，保证最后是对的。
- **评论本人看不到自己的评论：** 这是没做读己所写，作者读到了还没同步的副本。
**业务场景。** 跨境支付系统网络分区时，余额查询返回缓存里的旧值；扣款请求则拒绝或排队，等分区恢复后再处理，避免分区两侧各扣一次。
**系统设计。** [[links.tt-live-gift-coin-settlement|直播虚拟礼物：金币记账与主播结算]]：被问「送礼扣币和主播收益展示怎么取舍」，答扣币是资金变动，选一致；主播收益榜可以稍延迟，选可用加最终一致。
**可能问法。**
- 怎么按业务选 CP 还是 AP？ → 看出错的代价，并且按操作而不是整个系统取舍。一致性的代价是变慢或不可用，可用性的代价是短暂的错误数据，哪个小选哪个：扣款宁可拒绝也不能多扣少扣，选一致；评论、点赞短暂不准无妨，选可用加最终一致。
- 点赞计数为什么可以不强一致？ → 点赞数短暂差几个，用户几乎感知不到，也没有资金损失；强一致要同步协调，代价是变慢甚至不可用。所以点赞异步落库，计数最终一致，换来高可用和高吞吐。
- 评论怎么做到本人立即可见？ → 用读己所写（read-your-writes）：发评论先写成功，作者本人写后的读取走主库或本地缓存，立即能看到；其他人读副本，晚几秒可见即可，这是可用加最终一致。
