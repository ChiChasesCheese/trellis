---
id: architecture-distributed-monolith
node: architecture.services
type: qa
---
## Q
Name the symptoms that reveal a "microservices" system is actually a distributed monolith, and the one-question test.

## A
Symptoms:

- Services must be **deployed together** or in a fixed order (lockstep releases, coordinated version matrices).
- **Shared database** or shared internal libraries that force simultaneous upgrades.
- One feature change touches **N repos**; chatty fine-grained synchronous calls ([[architecture-sync-call-chains]]).

Test: **"Can this team deploy its service alone, right now, without asking anyone?"** If not, you've kept the monolith's coupling and added network failures, latency, and operational overhead ([[architecture-microservices-tax]]) — strictly worse than either clean option. Fix by re-drawing boundaries around data ownership, or honestly merging back.

## Q zh
命名揭露"微服务"系统实际上是分布式整体的症状，一个一问题测试。

## A zh
症状：

- 服务必须**同时部署**或按固定顺序（lockstep 版本、协调版本矩阵）。
- **共享数据库**或强制同时升级的共享内部库。
- 一个功能改变触及**N 个 repos**；啰嗦细粒度同步调用（[[architecture-sync-call-chains]]）。

测试：**"这个团队可以单独部署其服务，现在，无需问任何人吗？"** 如果不是，你保持了整体的耦合并添加了网络故障、延迟和操作开销（[[architecture-microservices-tax]]）——严格比要么干净选项更坏。通过重新绘制围绕数据所有权的边界或诚实地合并回来修复。
