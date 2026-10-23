---
id: hl-j16-skiplist-experiment
node: java21.j16-concurrency-primitives
type: qa
step: 34
---
## Q
4 个线程各 5 万次随机挂单到 `ConcurrentSkipListMap<Long, Long>`（价格 18950–19049），怎么原子累加每个价位的数量？`pollFirstEntry` 有什么用？

## A
用 `merge(price, 1L, Long::sum)` 原子累加该价位数量。结果：价位数 100，总量 200000（期望 200000，守恒）；`firstEntry` 即最优卖价（18950=1988），`lastEntry` 即最高卖价（19049=1987）。

`pollFirstEntry` 是一步**原子**「取走并删除」最优档：取走 18950 后最优变成 18951。`tailMap`/`ceilingEntry` 可取价位 ≥ 某价的若干档。
