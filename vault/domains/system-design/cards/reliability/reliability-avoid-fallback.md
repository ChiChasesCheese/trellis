---
id: reliability-avoid-fallback
node: reliability.resilience.containment
type: qa
---
## Q
Why do fallback paths ("if the primary fails, switch to the backup logic") tend to fail exactly when they are needed, and what do teams like Amazon's do instead of writing them?

## A
Fallback code fails when needed because of three compounding properties:
- **Untested**: it runs so rarely that it bit-rots; the first real execution is during your worst outage.
- **Cold**: its caches are empty, connections unopened, capacity unprovisioned — it starts from zero under peak demand.
- **Triggered under stress**: the very condition that trips it (overload, dependency failure) is the worst environment for novel behavior, and a bimodal system (a normal mode and a rare emergency mode) means the emergency mode is by definition the unverified one.

Instead:
- **Fail fast** and return the error — let the caller's existing retry/timeout machinery handle it.
- **Keep one path** and make it excellent: harden the primary rather than maintaining a second-rate twin.
- **Promote the fallback to always-on**: if the backup work matters, do it on every request (constant work), so it is exercised, warm, and provisioned.
- **Static stability**: keep operating on last-known-good data when a dependency disappears, rather than switching to new logic.

## Q zh
为什么 fallback 路径（"主路径失败就切到备用逻辑"）往往恰好在需要的时候失效？Amazon 这类团队不写它们，改做什么？

## A zh
Fallback 代码在需要时失效，源于三个相互叠加的性质：
- **未经测试**：它极少运行所以会腐烂（bit-rot）；第一次真实执行就发生在你最糟的故障中。
- **冷启动**：它的缓存是空的、连接没建立、容量没预置 — 在峰值需求下从零开始。
- **在压力下触发**：触发它的条件（过载、依赖故障）本身就是最不适合运行新行为的环境；而双模系统（一个正常模式加一个罕见的应急模式）意味着应急模式定义上就是未经验证的那个。

替代做法：
- **Fail fast**，直接返回错误 — 交给调用方已有的重试/超时机制处理。
- **只保留一条路径**并把它做到极好：加固主路径，而不是维护一个二流的孪生兄弟。
- **把 fallback 升格为常开**：如果备用工作真重要，就每个请求都做（constant work），让它被持续演练、保持温热、容量已备。
- **Static stability（静态稳定）**：依赖消失时继续用最后已知良好的数据运行，而不是切换到新逻辑。
