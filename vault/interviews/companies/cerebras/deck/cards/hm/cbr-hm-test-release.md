---
id: cbr-hm-test-release
node: hm.test-strategy
type: qa
step: 2
---
## Q
面试题：你会怎么验证一次推理软件栈的发布（发布候选）？按顺序答。

## A
1. **Entry**: release candidate cut; each feature's **own qualification** done; **known issues** written down.
2. **Risk map**: diff vs last release — compiler, runtime, kernels, firmware, models. **New interactions** get new scenarios; the rest get standing regression.
3. **Evidence**: unit, simulation, benchmark, feature and integration results **in one view**; gaps **named**.
4. **Matrix by risk**: models × sizes × context lengths × batch sizes, weighted by **what customers run**.
5. **Triage**: every failure **classified** — real regression, flaky, environment, infrastructure, known; real ones **bisected** to a commit with an owner.
6. **Exit**: no open blockers; performance and accuracy within thresholds; **upgrade and rollback** tested; a written **go/no-go with explicit gaps**.
7. **After rollout**: first-pass triage; every **escaped defect** gets a test **at the right layer**; track escape rate, time to triage, master green rate.

```mermaid
flowchart TD
    A["1 Entry: RC 切出, 各功能验证完, 已知问题记下"] --> B["2 Risk map: 和上次发布比 diff"]
    B --> C["3 Evidence: 五类结果放进一个视图"]
    C --> D["4 Matrix: 按客户在跑的加权"]
    D --> E["5 Triage: 每个失败分类, 真回归 bisect"]
    E --> F["6 Exit: 无阻塞, 阈值内, 升级回滚已测, 书面 go/no-go"]
    F --> G["7 上线后: 首轮排查, 漏网缺陷补到正确的层"]
```

> 中文提示：**批大小（batch size）**= 一次一起算的请求数。结尾连到你的质量门："checks are entry criteria, a status is the exit."
