---
id: bagu-follow-feed-1-push-pull-bigv
node: b.scenario.follow-feed
type: qa
step: 1
---
## Q
**关注关系与 Feed 流 · 推拉结合与大 V 问题**｜追问

面试官：「刷抖音关注页：关注关系怎么存才能快速查询？Feed 用推、拉还是推拉结合？大 V 发作品会遇到什么问题？」

## A
**基本回答。** 关注关系存两份：「我关注了谁」按关注者分片，「谁关注了我」按被关注者分片，两种查询都落单分片。推（写扩散）是发布时写进每个粉丝的收件箱，读快、写重、存储大；拉（读扩散）是读时合并所关注者的作品，写轻、读重，关注越多越慢。普通用户推，大 V 拉：大 V 千万粉丝发一条要写千万次收件箱（写放大），队列和延迟扛不住，所以大 V 只存自己的发件箱，读时归并（也可只推给活跃粉丝）。收件箱用 Redis ZSet 按时间排序、限长几百条；翻页用游标不用 offset。关注和取关写消息队列异步构建倒排表和索引，代价是取关后短时间内可能还看得到（最终一致）。图数据库只有「好友的好友」这类多跳查询才值得，还多一套存储要运维。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 278">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">推：普通用户发作品</text>
<rect x="6" y="48" width="64" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38.0" y="66.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">作者</text>
<rect x="110" y="22" width="104" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="162.0" y="38.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粉丝 1 收件箱</text>
<line x1="70" y1="62" x2="108" y2="34" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,34.0 104.3,40.7 100.5,35.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="110" y="54" width="104" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="162.0" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粉丝 2 收件箱</text>
<line x1="70" y1="62" x2="108" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,66.0 100.7,68.4 101.4,62.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="110" y="86" width="104" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="162.0" y="102.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">粉丝 3 收件箱</text>
<line x1="70" y1="62" x2="108" y2="98" stroke-width="1.2" stroke="currentColor"/>
<polygon points="108.0,98.0 100.7,95.5 105.1,90.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="226" y="60" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读快、写重</text>
<text x="226" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写放大</text>
<text x="8" y="134" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">大 V 千万粉丝：一条要写千万次</text>
<text x="8" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">拉：大 V 不推，读时合并</text>
<rect x="6" y="166" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大 V 发件箱</text>
<rect x="6" y="204" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56.0" y="222.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">我的收件箱</text>
<rect x="136" y="184" width="104" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="188.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">读时按时间归并</text>
<rect x="268" y="184" width="66" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="301.0" y="202.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Feed</text>
<line x1="106" y1="180" x2="134" y2="194" stroke-width="1.2" stroke="currentColor"/>
<polygon points="134.0,194.0 126.3,193.7 129.2,188.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="106" y1="218" x2="134" y2="204" stroke-width="1.2" stroke="currentColor"/>
<polygon points="134.0,204.0 129.2,210.0 126.3,204.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="240" y1="198" x2="266" y2="198" stroke-width="1.2" stroke="currentColor"/>
<polygon points="266.0,198.0 259.0,201.2 259.0,194.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="254" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">收件箱：Redis ZSet，限长，游标翻页</text>
<text x="8" y="272" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">也可大 V 只推给活跃粉丝</text>
</svg>
上半部分是推：普通作者发布时作品写进每个粉丝的收件箱。下半部分是拉：大 V 作品只存在自己的发件箱，粉丝读 Feed 时把大 V 发件箱和自己的收件箱按时间归并。
**举个例子。** 小明关注了小红（100 粉丝）和一位大 V（一千万粉丝）：小红发作品写 100 次收件箱；大 V 只写自己的发件箱 1 次；小明刷新时取收件箱，再拉大 V 发件箱，按时间归并取前几条。offset 翻页的问题：第一页时间序 100、99、98，此时有人发新作品变成 101、100、99、98、97，offset 3 取到 98、97、96，98 重复；游标「时间小于 98」则不论插入多少新内容都得 97、96、95。
**容易错。**
- **全部用推：** 大 V 一条写千万次。
- **全部用拉：** 关注很多人时要合并太多路。
