---
id: pay-correctness-distributed-transactions-tcc
node: correctness.distributed-transactions
type: qa
step: 4
---
## Q
TCC（Try-Confirm-Cancel）是什么？空回滚和悬挂是什么问题，怎么处理？用钱包余额支付举例。

## A
**TCC**：每个参与方提供三个接口。
- **Try**：检查并**预留**资源，但不真正提交。
- **Confirm**：把预留变成正式提交。
- **Cancel**：释放预留。

**例子：用钱包余额买商品，账户余额 100，订单 30**
1. Try：钱包服务冻结 30（账面 100，可用 70，冻结记录 `hold_1` 状态 active）；订单服务把订单置为"待确认"。
2. 全部 Try 成功 → 调用 Confirm：冻结转扣款，写分录；订单确认。
3. 任一 Try 失败 → 调用 Cancel：冻结释放，订单取消。

**两个经典问题**
- **空回滚**：Try 请求因网络问题没到达（或超时），协调者已发出 Cancel，参与方收到 Cancel 时根本没有预留记录。Cancel 必须允许"没有 Try 记录也成功返回"，并**记录这次 Cancel**。
- **悬挂**：Cancel 先到并处理完，之后迟到的 Try 才到达，把资源预留上了，却再无人确认或取消。解决：Try 先检查是否已有该事务的 Cancel 记录，有则拒绝。

**还要保证**：三个接口都幂等（事务 id + 状态记录），Confirm 和 Cancel 必须能重试到成功。

**适用与限制**
- 适合内部、可预留的资源：余额、库存、优惠券。
- 外部渠道扣款通常没有"Try"这一步（授权加请款是最接近的类比：授权就是 Try，请款是 Confirm，撤销授权是 Cancel）。
- 代价：业务侵入大，每个服务都要实现三个接口和状态记录。
