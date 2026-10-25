---
id: pay-card-lifecycle-tokenization-psp-vault-token
node: card-lifecycle.tokenization
type: qa
step: 3
---
## Q
PSP 金库令牌（vault token）怎么工作？它带来的最大工程隐患是什么？

## A
**工作方式**
1. 用户在 PSP 提供的托管输入框（或移动 SDK）里输入卡号，卡号直接发到 PSP，不经过你的服务器。
2. PSP 把卡号存进自己的金库，返回一个令牌，如 `tok_1abc`（示意）。
3. 你的后端保存令牌，与用户、支付方式 id 关联。
4. 以后用这个令牌向同一个 PSP 发起授权，PSP 在金库里查出真实卡号，转发给收单行。

**优点**
- 你的系统几乎不接触卡数据，PCI 范围最小。
- 实现快，PSP 通常还自带卡到期更新、账户更新服务。

**最大隐患：令牌与 PSP 绑定（lock-in）**
- 令牌只对发行它的 PSP 有意义。换 PSP，或要接第二家 PSP 做容灾，旧令牌用不了。
- 迁移需要 PSP 配合导出卡号到新 PSP（PCI 对 PCI 的数据迁移），有的 PSP 不愿意、有的收费，过程长且有风险。
- 如果不迁移，只能让用户重新输入卡号，订阅用户大量流失。

**应对**：设计内部稳定的"支付方式 id"（payment_method_id）作为业务引用，映射到各渠道令牌；一开始就规划多 PSP 与迁移路径，或使用独立于 PSP 的令牌金库。
