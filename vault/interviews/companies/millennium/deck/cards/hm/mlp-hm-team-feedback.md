---
id: mlp-hm-team-feedback
node: hm.teamwork
type: qa
step: 3
---
## Q
**接受批评与推翻自己**｜经理面与行为面

“Tell me about a time you received critical feedback. What did you change?”

## A
用主动推翻自己的那次：先说出自己的数字错了，再重做。再配一个自己设计里的缺陷作备用。

- **主故事：** 大型电商商户切到净额结算（net settlement）后，部分退款费带着旧的月度 billing terms。你第一版影响范围查询给出约 196K 行、61 商户、$11K。
- **纠错：** 在别人据此行动之前，你重审谓词，发现它没检查“新定价计划在费用创建时已存在”，很多行的计划是几个月后回填的，写入时本来就对。加上一个条件后，真实范围是 21,923 行、30 商户、$5,854。
- **根因：** 退款费路径复制了 credit 的历史计划编号，没有在费用创建时解析生效计划。顺带发现上游一个 1.5 小时的写入滞后。
- **备用：** 自己设计的质检框架按表级放行，约 50 个坏商户挡住 35,000 个；你写了 ADR 提出降到商户级。

**英文答法。**
- My first blast-radius query said about **two hundred thousand** fee rows across **sixty merchants**.
- Before anyone acted, I re-checked the predicate: it didn't test that the **new pricing schedule existed at fee-creation time**, so many rows were already correct.
- Adding that condition gave **about twenty-two thousand rows, thirty merchants, under six thousand dollars**.
- I'd rather **retract my own number in public** than have a remediation sized off a bad predicate.

**追问。**
- **What was the root cause?** The refund-fee path copied the credit's historical schedule id instead of resolving the effective schedule at fee time.
- **What did you change afterwards?** Every claim now comes with a re-runnable query, so the next person can audit it.
- **Another example?** My own readiness design blocked **thirty-five thousand** merchants because of about **fifty** bad ones; I drove an ADR to make it merchant-level.
