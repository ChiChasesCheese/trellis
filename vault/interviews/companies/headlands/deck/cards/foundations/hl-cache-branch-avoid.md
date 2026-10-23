---
id: hl-cache-branch-avoid
node: foundations.cpu-cache-locality
type: qa
step: 30
---
## Q
热循环里的数据相关分支怎么避免？低延迟交易系统在热路径上怎么处理分支？Java 有 `likely` 提示吗？

## A
避免分支的办法：
- 用算术代替判断，如 `sum += (v >= 128 ? v : 0)` 常被编译成 csel；
- 查表代替 `switch`（`int[]` 查表，解码一次，无分支）；
- 数据按类别分开，先分区再处理，不在循环里判断。

低延迟交易系统：**热路径**（收到行情后决定下单的路径）里几乎不出现不可预测的分支，罕见情况（错误处理、日志）放冷路径，热路径上「最常见的情况」应总是同一走向。

Java 没有 `__builtin_expect` / `likely` 提示，JIT 按运行时分支统计自己排布代码（热路径放一起）。
