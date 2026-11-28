---
id: bagu-gap-deadlock-1-lock-kinds
node: a.mysql.gap-deadlock
type: qa
step: 1
---
## Q
**行锁的三种形态 · 记录锁、间隙锁、next-key 锁**｜必会

面试官：「InnoDB 的行锁有哪几种形态？间隙锁和 next-key 锁是什么，为什么需要它们？」

## A
**基本回答。** InnoDB 的行锁加在索引记录上，有三种形态：记录锁（record lock）只锁一条索引记录；间隙锁（gap lock）锁两条相邻记录之间的空隙，不含记录本身，作用是阻止别人往里插入；next-key 锁是记录锁加上它前面的间隙，区间左开右闭，例如对 20 加锁，锁的是 `(10, 20]`。间隙锁和 next-key 锁只在 RR 下对当前读生效，目的是防幻读。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 208">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">索引上已有记录 1、5、10：</text>
<rect x="30" y="26" width="30" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="45.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="120" y="26" width="30" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="210" y="26" width="30" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="225.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="60" y="26" width="60" height="30" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="90.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(1,5)</text>
<rect x="150" y="26" width="60" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(5,10)</text>
<rect x="240" y="26" width="60" height="30" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="270.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(10,+∞)</text>
<line x1="120" y1="76" x2="150" y2="76" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="114" y="80" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">记录锁 5</text>
<line x1="150" y1="94" x2="210" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="144" y="98" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">间隙锁 (5,10)</text>
<line x1="150" y1="112" x2="240" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="144" y="116" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">next-key (5,10]</text>
<text x="8" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">事务 A：WHERE id=6 FOR UPDATE，没命中</text>
<text x="8" y="170" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">锁住 (5,10)：别人插入 7、8、9 被挡</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读写已有的 1、5、10 不受影响</text>
</svg>
索引上有 1、5、10 三条记录（方格），方格之间是间隙；高亮的是 (5,10) 这一段。下面三条线分别表示：记录锁只锁 5，间隙锁锁 (5,10)，next-key 锁锁 (5,10]（连 10 一起）。
**举个例子。** 订单号现有 1、5、10，事务 A 执行 `SELECT ... WHERE id = 6 FOR UPDATE`：
1. **没命中任何行：** id=6 不存在，但 InnoDB 仍要保证「再查一次也还是没有 6」。
2. **锁住间隙：** 6 落在 5 和 10 之间，所以锁住 `(5, 10)` 这一段。
3. **别人插入被挡：** 事务 B 想插入 7、8、9，被阻塞，直到 A 结束。
4. **已有记录不受影响：** 读写已有的 1、5、10 照常进行，因为间隙锁不锁记录本身。
5. **换成 RC：** 同样的语句没有间隙锁，B 可以直接插入 7。
**容易错。**
- **以为间隙锁会锁住已有的行：** 间隙锁只锁空隙，不含记录；读写已有记录不受影响。
- **以为两个间隙锁会互相冲突：** 它们不互斥，只和「往间隙里插入」冲突，所以才会出现两边都拿到、又互相阻塞的死锁。
- **以为 RC 下也有间隙锁：** RC 基本没有（外键和唯一键检查除外）。
- **以为没命中就不加锁：** 没命中任何行的等值当前读，也会锁住所在的间隙。
