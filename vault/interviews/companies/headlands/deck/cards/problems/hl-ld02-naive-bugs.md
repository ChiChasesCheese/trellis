---
id: hl-ld02-naive-bugs
node: problems.ld02-trading-ood
type: qa
step: 12
---
## Q
最天真的交易系统写法（`HashMap<String, Order>`、`double`、字符串状态）暴露哪些问题？

## A
天真版：`Order` 用 `String side`、`double qty/price`、`String status="NEW"`；`onFill` 里 `o.filled += q`，`>= qty` 就置 `"FILLED"`；`position.merge(symbol, BUY?q:-q, Double::sum)`；风控只看 `qty > 1000` 和净仓 `|pos ± qty| <= 3000`。

| 输入 | 暴露的问题 |
|---|---|
| 同一个 `Fill` 投递两次 | 仓位翻倍；`filled` 超过 `qty` |
| `CANCELED` 的订单又收到 `Fill` | 悄悄改回 `PARTIAL`——幽灵订单 |
| `side = "buy"`（小写）/ 拼错状态 | `equals` 不匹配，被当卖单；编译器不提醒 |
| 数量 0.1 + 0.2 | `double` 误差，订单永不到 `FILLED` |
| 多头 10 股，卖 25 股 | `merge` 只得 −15，**盈亏没算**：无「平 10 股的实现盈亏」，无新空头的成本 |
| 风控：已有挂单 | 只看 position 不看未成交挂单，最坏情况仓位漏了 |
| 风控检查时订单已登记 | 把自己算进未完成数量，顶格订单被误拒 |
| 订单数很多 | 每次扫描所有订单求未完成数量，总 O(n²) |
| 重启 | 状态全丢，无恢复手段 |

对应改进（9 步）：类型表达不变量 → 显式状态机（非法转移抛异常且不改状态）→ Fill 去重在状态检查之前 → 聚合量增量维护 → 仓位 FIFO lot 队列 → 风控整数交叉相乘、溢出视为拒绝 → 最坏情况仓位 → 装配成 `TradingDesk` 输入先记日志 → 重放吞掉同样的异常。

常见误区汇总：
1. 先登记订单再做风控检查；
2. 重复回报按状态检查（订单 FILLED 后的旧回报被当非法转移抛异常，或更糟当新成交把仓位翻倍）；
3. 边验证边修改；
4. 用 `double` 或 `int`（`int` 的 `qty × px` 在 21 亿就溢出）；
5. 翻转时只改方向不算盈亏；
6. 风控只看净仓不看挂单；
7. 价格带用除法 / 浮点（边界误拒误放，参考价 3 时 5% = 0.15 整除出 0）；
8. 缺参考价就放行（fail open）；
9. `replay` 里不吞异常；
10. `journal()` 返回内部 list；`PENDING` 订单没计入未完成。
