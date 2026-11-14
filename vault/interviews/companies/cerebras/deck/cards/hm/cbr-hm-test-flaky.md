---
id: cbr-hm-test-flaky
node: hm.test-strategy
type: qa
step: 3
---
## Q
面试题：How do you deal with flaky tests? 按说出口的顺序怎么答？

## A
1. **Measure first**: rerun to get a **pass rate**; a test that passes 95% of runs on the same commit is flaky, not "unlucky".
2. **Quarantine, don't delete**: move it to a **separate lane** so it stops blocking master, with an **owner** and a **deadline**.
3. **Find the cause**: shared state, **time** and ordering, **concurrency**, test environment, external services, resource limits.
4. **Retries are diagnosis, not a fix**: auto-retry hides real intermittent bugs — like a race in a runtime.
5. **Kill the class**: make state **deterministic**. "My schema pool did that: test state came from the **deployed commit**, never from **who ran last**."
6. **Track it**: flake rate per test and per suite, so master's signal stays **trustworthy**.

```mermaid
flowchart TD
    A["1 重跑, 量出通过率"] --> B["2 隔离到单独通道: 有负责人和期限"]
    B --> C["3 找原因: 共享状态, 时间, 并发, 环境等"]
    C --> R["4 重试只用来诊断, 不算修复"]
    R --> D["5 消灭这一类: 状态确定化"]
    D --> E["6 按测试和套件跟踪 flake rate"]
```

> 中文提示：这正是 RIT 职位里的"distinguish real regressions from flakiness"。在推理里还要加一条：浮点结果随运算顺序变化，比较要用容差，否则会制造假 flaky。
