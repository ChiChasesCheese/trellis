---
id: reliability-timeout-budget-arithmetic
node: reliability.resilience.retries
type: qa
---
## Q
Gateway → A → B → C, each hop with a 1s timeout and 3 attempts, under a 3s user-facing budget. Do the arithmetic and give the configuration rules.

## A
Retries **multiply down the stack**: C can take 3×1s = 3s; B wraps that in 3 attempts → 9s; A → 27s. The user's 3s budget is blown 9× over, and the extra attempts arrive at an already-sick C as 27× load.

Rules:
- **Retry at one layer only** — usually the one closest to the failure that can still classify the error, or the outermost that owns the budget. Never at every hop.
- Size the **per-attempt timeout from the dependency's p99 (times ~1.5–2)**, not from the mean and not from a framework default of 30–60s; a default-timeout client is how thread/connection pools get exhausted.
- **Total budget, not per-hop**: `attempts × per-attempt timeout ≤ remaining budget`, and each hop passes down its *remaining* time so inner deadlines are always strictly shorter than outer ones.
- Before starting an attempt, check the remaining budget against the dependency's **p50** — if it can't plausibly finish, fail fast instead of spending capacity on a request nobody will read.

## Q zh
Gateway → A → B → C，每个 hop 有一个 1s timeout 和 3 次尝试，在 3s 用户面对预算下。做数学计算并给出配置规则。

## A zh
重试**乘以向下堆栈**：C 可以取 3×1s = 3s；B 包裹那在 3 次尝试 → 9s；A → 27s。用户的 3s 预算被吹 9 倍，额外尝试作为 27 倍负载到已经生病的 C。

规则：
- **仅在一层重试** ——通常是最接近故障但仍能分类错误的那个，或拥有预算的最外层。永不在每个 hop。
- 从依赖的 **p99（次 ~1.5–2）**大小**每次尝试 timeout**，不是从平均值和不是从框架默认 30–60s；默认 timeout 客户端是线程/连接池如何获得耗尽。
- **总预算，不是每 hop**：`attempts × per-attempt timeout ≤ remaining budget`，每个 hop 向下传递其*剩余*时间所以内 deadline 总是严格短于外。
- 在启动尝试前，检查剩余预算对依赖的**p50** ——如果它不能似乎完成，快速失败而不是花容量在没人会读的请求。
