---
id: nr-amz-g2-starl
node: amazon.g2
type: qa
step: 1
---
## Q
【让正确性不依赖 agent 的自述（senior 机制故事）】适用 LP、开场 hook 和 STAR-L 提纲

## A
- 主 LP：Insist on the Highest Standards；备用：Invent and Simplify（机制简单到一条命令）、Ownership、Are Right, A Lot。

**Hook：「A green suite isn't proof, so I test the tests.」**

- **S · Situation**
    - I produced about **100 interview-prep artifacts**: **49 system-design** and **45 low-level-design** problems, via **parallel Claude Code subagents**.
    - A model that grades its own work says "**done**" every time.
- **T · Task**
    - Make correctness **independent of the agent's word**.
    - It must **scale** to more agents without me re-reading everything.
- **A · Action**
    - I rejected **self-reports plus a spot check**.
    - **One agent owns one directory**; **three at a time**.
    - I wrote the **acceptance gate as a command** before any content: reference solution must **pass**, empty starter must **fail**.
    - I also rejected **agents reviewing agents**: one spawned a reviewer and broke my cap, so "**never start another agent**" became a rule.
    - I **re-run the gate myself**, **re-derive every number**, and read the agent's **weakest-claims list**; every defect becomes a **rule**.
    - **Later**, to test the tests, I used **mutation**: on one kata, a **concatenated-key** bug passed all **10 tests**.
    - I added the missing assertion; the suite now kills **11 of 11** hand-written mutants.
- **R · Result**
    - **45 of 45** LLD problems and about **900 tests** passed.
    - **Nine** drafts went back for rework.
- **L · Learning / Mechanism**
    - Verification has to be a **mechanism, not a mood**.
