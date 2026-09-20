---
id: problems-flash-sale-undersell-vs-oversell
node: problems.commerce.flash-sale
type: qa
step: 7
tags: [grown]
---
## Q
Besides never overselling, a flash-sale system must also never 'undersell' — rejecting a legitimate purchase attempt while stock actually remains. Name two concrete design mistakes that cause undersell, distinct from the mistakes that cause oversell.

## A
First, setting the admission-control rate limiter too conservatively (well below what the downstream inventory check and database can actually sustain) causes legitimate buyers to be rejected at the admission layer even though stock and database capacity remain available. Second, a reservation-expiry sweep that runs too infrequently relative to the reservation TTL leaves already-abandoned reservations occupying inventory for too long, making the system look sold out when it isn't. Oversell mistakes, by contrast, come from splitting the read-check-write into non-atomic steps or from having multiple independent inventory counters for the same SKU; undersell mistakes come from being unnecessarily conservative or slow to reclaim.

## Q zh
除了绝不超卖，秒杀系统也必须绝不「漏卖」——在库存明明还有的情况下拒绝了本该成功的合法购买请求。举出两个具体会导致漏卖、且和导致超卖的原因不同的设计失误。

## A zh
第一，把准入控制的限流速率设得过于保守（远低于下游库存判定和数据库真正能承受的水平），会导致明明库存和数据库容量都还有余量，合法买家却已经在准入层被拒绝。第二，保留过期扫描的执行频率相对保留有效期太低，会让早已被放弃的保留长期占着库存，让系统看起来「已售罄」实际上并没有。相比之下，导致超卖的失误来自把「读取-判断-写入」拆成非原子的多步，或者为同一个 SKU 设了多个各自独立的库存计数器；导致漏卖的失误则来自不必要的保守或回收得太慢。
