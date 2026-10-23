---
id: hl-hc09-hidden-pitfalls
node: problems.hc09-top-trades-by-notional
type: qa
step: 14
---
## Q
top-k notional 题的隐藏测试和常见误区有哪些？

## A
| 很多人会这样写 | 为什么错 | 正确 |
|---|---|---|
| 最大 k 个用最大堆装全部再弹 k 次 | O(n) 空间，不能流式 | 大小为 k 的**最小**堆 |
| 比较器只写 notional 降序 | 平局顺序未定义，并行后更乱 | 三级全序 |
| `comparing(A).thenComparing(B).reversed()` | B 也被反转 | `reversed()` 紧跟第一个条件 |
| 快速拒绝写成 `<=` | 平局时 ticker 更小的好事件被误拒 | 严格 `<` |
| `long notional = price * volume` | 溢出静默绕回 | `multiplyExact` |
| 只对进堆的事件检查溢出 | 检测与数据排列有关 | 每个事件都校验 |
| `double` 存金额并行累加 | 浮点不满足结合律 | 整数 tick |
| `TreeSet` 比较器只看总额 | 总额相同的 ticker 被吞 | 比较器带 ticker |
| 先改 `acc.total` 再 `ranking.remove(旧键)` | 找不到旧键，残留脏数据 | 先按旧值删，改，再按新值插 |
| 溢出检查放在改状态之后 | 抛异常时状态已被破坏 | 先 `addExact`，成功再改 |
| combiner 把 left 并进 right | left 内容丢了 | 并进第一个参数 |
| supplier 返回共享对象 | 数据竞争 | 每次 `new` |
| 取消时不检查中断标志 | 线程仍算到底 | 定期 `isInterrupted()` |
| `n*c/chunks` 用 `int` | `n*c` 溢出 | 先转 `long` |

其他：零 notional 的 ticker 丢失（出现过但总额 0 的 ticker 要存在）；窗口边界差一；总额溢出后状态损坏；失败后不取消其余块；输出 poll 后 `reversed()` 位置放错。

**边界清单**：空数组；`k = 0`；`k > n`；单个事件；notional 相同 ticker 不同；notional 与 ticker 都相同；价格或数量为 0 的事件合法排最后；`Long.MAX_VALUE × 2`；`3037000499²` 通过而 `3037000500²` 溢出；同一 ticker 两个 `MAX/2+1`；恰好等于 `Long.MAX_VALUE`；数组长度不等；负价格；null ticker；`k < 0`；窗口 0；时间倒退；块数多于事件数；块边界把同一 ticker 的两笔分开使得合并才溢出；打乱事件顺序结果不变。
