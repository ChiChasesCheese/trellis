---
id: hl-hc02-lazy-iterator
node: problems.hc02-merge-k-streams
type: qa
step: 7
---
## Q
惰性合并迭代器（`mergeIterators`）要满足哪些规则？为什么输出元素后要推迟补位？

## A
迭代器 `Iterator<T>`（`hasNext()` / `next()`）的元素可用到时才生产，所以能处理比内存大、无限、来自网络的数据。合并迭代器规则：
1. **构造时不取任何元素**（构造函数不该有副作用或阻塞）；
2. 第一次 `hasNext()/next()` 才给每个 source 取一个队首入堆；
3. `next()` 弹出堆顶返回，把它来自的序列记成 `lastEmitted`，**不立刻取下一个**；
4. 下一次 `hasNext()/next()` 开头先给 `lastEmitted` 补位，再看堆。

原因：source 可能是慢流，取下一个可能等一秒；调用者此刻只想要已经能返回的 `x`，不该为还没要的元素白等。

可验证性质：消费 n 个元素后，所有 source 的 `next()` 总调用 ≤ **k + n − 1**（初始 k 次，最后一个输出的补位还没发生）；两个无限序列取前 10 个只读约 11 个。

`mergeStreams`：`StreamSupport.stream(Spliterators.spliteratorUnknownSize(it, ORDERED), false)` 包成 `Stream`，再 `onClose` 关闭所有输入，`.limit(5)` 只读够用的。
