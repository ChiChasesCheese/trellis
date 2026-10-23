---
id: hl-hc08-text-interface
node: problems.hc08-order-sequence-api
type: qa
step: 10
---
## Q
订单序列的文本接口格式是什么？用样例手跑一遍，包括出错的输出。

## A
命令：`PUT id qty`、`DELETE id qty`、`COUNT id`、`QTY id`、`AT k`。大小写不敏感、空白任意；`replay` 跳过空行和 `#` 行；格式错抛 `IllegalArgumentException`，信息以 `line N` 开头。输出：`PUT` → `OK`；`DELETE` → 剩余数量；`COUNT` / `QTY` / `AT` → 数字；业务错误 → `ERR <message>`（`unknown id`、`quantity exceeds remaining`、`duplicate id`、`index out of range`）。

实现：`parse` 用 switch 表达式 + `yield`（先 `args(t, 3)` 检查参数个数再 `yield new Put(...)`）；`apply` 对 sealed `Op` 做记录模式匹配，捕获四类异常转成 `Err`；`render` 对 sealed `Result permits Ok, Num, Err` 做穷尽 switch，`case Ok _ -> "OK"`。

样例：`PUT 10 5; PUT 20 3; PUT 30 7` 输出三个 `OK`；`COUNT 30` → 3；`QTY 20` → 8；`DELETE 20 3` → 0；`QTY 30` → 12；`AT 2` → 30；`DELETE 10 5` → 0，序列 `[30:7]`；`put 20 4` → OK，排最后 `[30:7, 20:4]`；`QTY 20` → 11；`DELETE 99 1` → `ERR unknown id`；`DELETE 30 9` → `ERR quantity exceeds remaining`；`PUT 30 1` → `ERR duplicate id`；`AT 3` → `ERR index out of range`；`AT 2` → 20。

部分删除样例：`PUT 1 10; PUT 2 10; PUT 3 10; DELETE 2 4` → 6；`QTY 3` → 26；`COUNT 3` → 3；`DELETE 2 6` → 0；`COUNT 3` → 2；`AT 2` → 3。原因：`DELETE 2 4` 只是减量（10→6），订单还在序列里，`COUNT 3` 仍是 3；再删 6 才真正移除。

接口细节：`new OrderSequence()` 初始容量 16；`new OrderSequence(n)` 向上取整到 2 的幂（`n ≤ 0` → IAE）；`capacity()`、`compactions()` 可观察。
