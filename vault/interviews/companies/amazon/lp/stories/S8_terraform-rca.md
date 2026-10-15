# S8 · Terraform grant-ownership 7 分钟 RCA（压力下 debug · 主动指出下一个雷）

> 来源：`core/stories/S8 Terraform 7 分钟 RCA.md`（status: verified）。
> 主 LP：**Bias for Action · Dive Deep**；副：Ownership · Insist on the Highest Standards · Earn Trust · Deliver Results。
> 一句话：*"A release failed in QA; I was only cc'd, posted the root cause and fix seven minutes later, then scanned the whole repo and flagged the next two failures."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| 7 分钟 | 从被 cc 到贴出根因 + 修法 + 邻近模块核查 |
| QA → pre-prod → prod 同天部署 | 结果 |
| 全仓库扫描：79 个 ownership 资源，42 个缺 `outbound_privileges` | 事后扫描 |
| 多数是无害的 `future_*` 变体；另一模块 **2 个** 与出事的形状完全相同、尚未触发 | 风险 |
| PR snowglobe-terraform #1326；Slack #treasury-services-releases 2026-08-13 | 锚点 |

⚠️ 面试里曾说过 "the only resource in the whole repo missing it"——**不成立**。现在的说法：「I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet.」

## 2. 60–90 秒口播版（≈ 170 词）

> A release of our Snowflake infrastructure repo failed in QA. `GRANT OWNERSHIP` on a database was rejected because a reviewer role already held a dependent `USAGE` grant. Someone else was assigned to investigate; I was cc'd. Seven minutes later I'd posted the root cause — the ownership resource didn't set `outbound_privileges`, so Terraform tried to transfer ownership without revoking dependents — the one-line fix, `outbound_privileges = "REVOKE"`, and a check of neighboring modules. I asked whether I could push, the PR went in, and QA, pre-prod and prod deployed that afternoon.
>
> The part I care about is what came after. I scanned the whole repo: dozens of ownership resources lack the parameter — most are `future_*` grants where it's harmless — but two in another module are the exact same shape as the one that broke, and haven't fired yet. I flagged them. I'd rather own "here's the next one" than only the one that paged.

## 3. 2 分钟版（≈ 260 词）

> **Situation.** The release pipeline for our Snowflake infrastructure repo failed in QA, blocking a deploy. Snowflake rejected a `GRANT OWNERSHIP` because the target already had a dependent grant held by a reviewer role.
>
> **Why it happens.** Snowflake requires dependent grants on an object to be revoked before ownership can transfer. The Terraform provider expresses that as `outbound_privileges` set to `REVOKE` or `COPY`; omit it and apply is rejected. Terraform has no transactions, so a failed apply leaves partial state; fixes must be re-entrant.
>
> **Action.** I was cc'd, not assigned. I read the error, matched it to the grant structure I knew from the repo, and in seven minutes posted: root cause, the fix — `outbound_privileges = "REVOKE"` — and a check of adjacent modules. I asked if I could push a PR; it was reviewed, and QA, pre-prod and prod were deployed the same day.
>
> **After.** "Fixed this one" and "eliminated this class" are different jobs. I scanned the whole repo: 79 ownership resources, 42 without the parameter. Most are `future_*` variants where it doesn't matter. But the `scheme_fees` module had two resources with the same shape as the one that failed. I flagged them before they fired.
>
> **Result:** same-day three-environment deploy, plus two known-risk items surfaced proactively.

> 说话边界：不要说 "only resource missing it"（Chi 之前面试说过，不成立）；只说「那天核查了相邻模块，事后扫了全仓库」。

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Bias for Action** (P) | "I was cc'd on a failed release, not assigned — seven minutes later the root cause and fix were in the thread." | 7 分钟；问一句可否推 PR；同天三环境 | — |
| **Dive Deep** (P) | "The error message pointed to a grant; the answer was a missing provider argument." | ownership 转移前必须撤销依赖授权；对 repo grant 结构有全局图景 | — |
| **Ownership** (S) | "After the fire was out, I scanned for the next one." | 79/42 的扫描；标出 scheme_fees 的 2 个 | 说 "only resource" |
| **Insist on the Highest Standards** (S) | "Fix this instance versus eliminate the class." | 扫描全仓库 | 没有"消灭这一类"的落地机制——诚实说"标出，未修" |
| **Earn Trust** (S) | "I walked back an overclaim I'd made earlier." | 自纠 "only resource" | — |

## 5. 追问（≥5）

1. **How did you get to the root cause in 7 minutes?** → 对整个 repo 的 grant 结构有全局图景；错误信息指向依赖授权；Provider 对应参数。
2. **Why REVOKE and not COPY?** → 【待 Chi 补：选 REVOKE 而非 COPY 的理由（COPY 会复制授权到新所有者）；若当时没权衡，如实说】
3. **What are the risks of this fix?** → Terraform 无事务；REVOKE 会撤销 reviewer 角色的 USAGE，需确认 reviewer 角色是否依赖它 【待 Chi 补：当时怎么确认的】
4. **Why didn't you fix the two risky ones?** → 【待 Chi 补：是标出未修、还是已提 PR？以事实为准】
5. **How would you prevent this class?** → 全仓库 lint/policy check（无事务环境里把问题前移到 plan 阶段）；推断，非已落地。
6. **Why the scan?** → "修完这一次"和"消灭这一类"是两件事。
7. **Terraform pitfalls?** → 重命名资源默认删了重建（`moved` block / `state mv`）；危险变更拆小、可重入。

## 6. Senior 升级点（bar = senior）

当前档位：**speed + proactive risk-spotting 是 senior 的起点**；缺 **mechanism（防复发的机制）与 influence**。
- 【待 Chi 补：那两个同形风险后来有没有人修？你有没有开 ticket / 推动 owner 去修？（没有机制 = 停在英雄行为）】
- 【待 Chi 补：这件事之后，团队是否在 CI 加了 plan 阶段的检查或 review 清单？】
- 升级句：「Seven minutes was the easy part; the useful part was telling the team where the next one was.」
