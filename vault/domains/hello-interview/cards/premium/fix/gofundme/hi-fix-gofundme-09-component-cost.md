---
id: hi-fix-gofundme-09-component-cost
node: fix.gofundme
type: qa
step: 9
---
## Q
**GoFundMe · 第 45:00 分 · 加组件：职责和新问题**｜复盘

面试官：「你加了 Redis、队列、事务。逐个说：它们各自带来什么新问题？你怎么处理？」

你会怎么回答？

## A
**当时的回答。**
- **说了名字：** 你提到 Redis 的原子自增、队列、事务和复制。
- **没有成对说：** 每个组件的职责和它带来的新故障没有放在一起讲，所以「哪一笔已经应用过」一直没有答案。
**差在哪。**
- **工具名不等于机制：** 队列会重放，自增会执行两次；只说名字，总额仍然不对。
- **前后不一致：** 前面的设计选择都讲了取舍，后来加的组件没有同样对待。
**应该这样说。**
- **一句话模板：** 「我加 X 是为了 Y，新问题是 Z，我这样处理。」每加一个就说一遍。
- **Redis：** 「加它是为了快速给出总额；新问题是副本可能和真相不一致；我只把它 SET 成持久化的值，丢了就重建。」
- **队列：** 「加它是为了把成功事件交给工作进程；新问题是会重发、会重放；我用 applied 表的唯一键吸收重复。」
- **事务：** 「加它是为了让插入 applied 和累加一起提交；新问题是热门活动的总额行要排队；按平均每秒 50、峰值 150 笔，行锁够用，再多拆子计数。」
- **复制：** 「加它是为了分担读；新问题是副本有延迟；页面读 Redis，对账读主库。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">我加 X 为了 Y；新问题是 Z；这样处理</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Redis · 快速给出总额</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：副本可能和真相不一致</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET 成持久化值，丢了就重建</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">队列 · 把成功事件交给工作进程</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：会重发、会重放</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">applied 表，唯一键，冲突跳过</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">事务 · 插入和累加一起提交</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：热门活动总额行排队写</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">峰值约 150 笔/秒，行锁够；再多拆子计数</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">复制 · 分担读、能切换主库</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：副本有延迟，读到旧值</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">页面读 Redis；对账读主库</text>
</svg>
白板上：四个组件各一块，每块三行：职责、新问题、处理。
**面试官可能接着问。**
- 能不能不加队列？ → 可以。在把状态改成 Success 的同一个事务里累加总额，规模小就够。队列的价值是让支付路径不等总额更新、让多个消费者互不影响；我先说不加的版本，再说为什么要加。
- 队列选哪个？ → 随便选一个，我只依赖「至少一次投递」，重复由 applied 表吸收，顺序也不重要。
- 每个组件都要讲这么细吗？ → 不必。时间紧就挑最容易出错的一个讲透，其余用一句话模板带过。
**同类题。**
- **News Feed、Ticketmaster、Uber：** 加缓存、队列、分片时都会被追问。
