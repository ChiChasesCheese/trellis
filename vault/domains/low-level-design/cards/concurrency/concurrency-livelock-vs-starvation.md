---
id: concurrency-livelock-vs-starvation
node: concurrency.hazards
type: qa
---
## Q
Deadlock, livelock, starvation: distinguish them by what the threads are doing and name the characteristic fix for livelock.

## A
- **Deadlock**: threads blocked forever, consuming no CPU; state never changes.
- **Livelock**: threads actively running and *changing state* but making no progress — e.g. both detect conflict, both back off, both retry in lockstep (the corridor dance). Fix: **randomized backoff/jitter** so retries desynchronize.
- **Starvation**: the system progresses, but *some* thread never gets the resource — unfair locks, reader floods starving writers, priority inversion. Fix: fair queuing / bounded waiting.

Discriminator: check CPU + state changes. Blocked & frozen = deadlock; busy & frozen = livelock; others progress while one lags = starvation.

## Q zh
Deadlock、livelock、starvation：按线程正在做什么来区分它们，并说出 livelock 的标志性修法。

## A zh
- **Deadlock**：线程永久阻塞，不消耗 CPU；状态再也不变。
- **Livelock**：线程在积极运行、而且*状态确实在变*，却没有任何进展 —— 比如双方都检测到冲突、都退让、又都同步重试（走廊对撞舞）。修法：**随机化退避/抖动**，让重试彼此错开。
- **Starvation**：系统整体在推进，但*某个*线程始终拿不到资源 —— 不公平锁、读者洪水饿死写者、优先级反转。修法：公平排队 / 有界等待。

判别式：看 CPU 和状态变化。阻塞且冻结 = deadlock；忙碌且冻结 = livelock；别人在前进只有一个掉队 = starvation。
