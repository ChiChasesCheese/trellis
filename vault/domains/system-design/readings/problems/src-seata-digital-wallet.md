---
nodes: [problems.commerce.digital-wallet]
url: https://seata.apache.org/blog/seata-tcc-fence/
---
# Alibaba Seata Resolves Idempotence, Dangling, and Empty Rollback Issues in TCC Mode

值得读：Apache Seata 官方博客给出了 TCC（Try-Confirm-Cancel）模式三个经典陷阱——
幂等、空回滚（Cancel 先到但 Try 从未发生）、悬挂（Cancel 先于延迟的 Try 到达并完成，
之后姗姗来迟的 Try 把资源永久挂起）——的具体机制和 Seata 的 `tcc_fence_log` 方案（按
条件更新的状态机，与业务操作同事务提交）。与本题解不同的地方在于：原文分别描述三个
问题各自的对策，本题解额外指出三者共享同一个根因（后到达的操作没有先查询本地状态就
执行），并把这套机制具体应用在钱包充值/提现这一"外部参与者只能走 TCC"的场景上。
