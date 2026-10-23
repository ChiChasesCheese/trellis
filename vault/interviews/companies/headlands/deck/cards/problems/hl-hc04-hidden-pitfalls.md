---
id: hl-hc04-hidden-pitfalls
node: problems.hc04-queue-mean-snapshot
type: qa
step: 15
---
## Q
队列均值与快照题的隐藏测试和常见误区有哪些？

## A
- 用 `double` 做 running sum（`1e16 + 1 + 1 − 1e16 = 0`，不是 2）；
- 用 `long` 累加：`Long.MAX_VALUE` 两个就溢出，均值变负且无异常；用 `Math.addExact` 抛异常也不对——要的是「正确」不是「报错」；
- `pop` 后和不「退回」：累加器一转 `BigInteger` 就不转回，性能塌；
- 空队列的 `getMean`：除以 0 得 `NaN` 被当成合法答案；
- 环形缓冲扩容直接 `Arrays.copyOf`，`head` 在中间时顺序全乱；
- `Mean` 没约分或分母可为负（`6/-4 ≠ -3/2`）；
- `Correct(List)` 不拷贝；
- 版本化时每个版本复制数组（2 万版本 168 ms，O(n²)，30 万版本超时）；
- 并发读分两次读 `sum` 和 `size`，或两个 `volatile` 字段；
- 纯自旋读者跑在虚拟线程上，写者被饿死。

**边界清单**：空队列 `pop/getMean`、弹空后再 push；和超过 `Long.MAX_VALUE` 再弹回小数（累加器不能卡在大数上）；负数、0、`Long.MIN_VALUE`（`-x`、`Math.abs` 溢出）；环形缓冲扩容时 head 不在 0；均值非整数要约分、符号只放分子；`snapshot` 不带数字（清空）；快照含 `Long.MAX_VALUE`；版本分叉。

量级：100 万次随机 push/pop + 每 8 次一个 `getMean` 远低于 2 s。
