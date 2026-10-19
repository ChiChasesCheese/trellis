# Terraform grant-ownership 7 分钟 RCA（压力下 debug · 主动指出下一个雷）

**A release failed in QA; I was only cc'd, posted the root cause and fix seven minutes later, then scanned the whole repo and flagged the next two failures.**

## 适用 LP

- 主：**Bias for Action**、**Dive Deep**
- 副：Ownership、Insist on the Highest Standards、Earn Trust、Deliver Results

## 数字

- **7 分钟**：从被 cc 到贴出根因 + 修法 + 邻近模块核查
- QA → pre-prod → prod **同天**部署
- 事后全仓库扫描：**79** 个 ownership 资源，**42** 个缺 `outbound_privileges`
- 多数是无害的 `future_*` 变体；`scheme_fees` 模块里 **2 个**与出事的形状完全相同、尚未触发
- 不要说 "the only resource in the whole repo missing it"，不成立。说：「I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet.」

## S / T / A / R / L

### S
- **Snowflake 基础设施**仓库的发布在 **QA** 失败：`GRANT OWNERSHIP` 被拒
- 一个 reviewer 角色已持有依赖的 **USAGE** 授权

### T
- 别人被**分配**去查，我只是 **cc**；但发布被卡住

### A
- **读错误**，对上我熟悉的授权结构
- **7 分钟**贴出根因：ownership 资源没设 `outbound_privileges`
- 贴**一行修法** `outbound_privileges = "REVOKE"` + **邻近模块**核查
- **问了**能否直接推；PR 合入
- **事后**扫**全仓库**找同样的遗漏
- 标出另一模块里 **2 个**同形、还没触发的资源

### R
- QA、pre-prod、prod **同一下午**部署
- 扫描：几十个缺该参数，多数是无害 `future_*`；挖出 **2 个真实风险**，我不说它们已修

### L
- **修这一个**和**消灭这一类**是两件事
- 宁可负责「这是下一个」

## 追问与回答

- **How did you get to the root cause in 7 minutes?**
  - 对整个仓库的 **grant 结构**有全局图景；错误信息指向**依赖授权**；provider 有对应参数
- **Why REVOKE and not COPY?**
  - COPY 会把授权复制给新所有者；其余见待补
- **What are the risks of this fix?**
  - Terraform **无事务**，修复必须可重入
  - REVOKE 会撤销 reviewer 角色的 **USAGE**，要确认它是否依赖
- **Why didn't you fix the two risky ones?**
  - 见待补
- **How would you prevent this class?**
  - 全仓库 **lint / policy check**，前移到 **plan 阶段**；尚未落地，别说成已有
- **Why the scan?**
  - 「修完这一次」和「消灭这一类」是**两件事**
- **Terraform pitfalls?**
  - **重命名资源**默认删了重建（`moved` block / `state mv`）；危险变更**拆小、可重入**

## 换个 LP 讲

- **Bias for Action**：被 cc 不是被分配，七分钟后线程里就有根因和修法；强调问一句可否推 PR、同天三环境
- **Dive Deep**：错误信息指向授权，答案是缺一个 provider 参数；ownership 转移前必须撤销依赖授权
- **Ownership**：火灭了之后我去扫下一个；79/42 的扫描，标出 scheme_fees 的 2 个；别说 "only resource"
- **Insist on the Highest Standards**：Fix this instance versus eliminate the class；扫全仓库；诚实说「标出，未修」，没有消灭这一类的落地机制
- **Earn Trust**：自己纠正之前说过的 "only resource" 夸大

## 待补

- 【待补：选 REVOKE 而非 COPY 的理由；若当时没权衡，如实说】
- 【待补：当时怎么确认 reviewer 角色不依赖被撤销的 USAGE】
- 【待补：那两个同形风险是标出未修，还是已提 PR；以事实为准】
- 【待补：那两个风险后来有人修吗，你有没有开 ticket / 推 owner 去修】
- 【待补：事后团队是否在 CI 加了 plan 阶段检查或 review 清单】

<details><summary>逐字稿</summary>

> A release of our Snowflake infrastructure repo failed in QA. `GRANT OWNERSHIP` on a database was rejected because a reviewer role already held a dependent `USAGE` grant. Someone else was assigned to investigate; I was cc'd. Seven minutes later I'd posted the root cause — the ownership resource didn't set `outbound_privileges`, so Terraform tried to transfer ownership without revoking dependents — the one-line fix, `outbound_privileges = "REVOKE"`, and a check of neighboring modules. I asked whether I could push, the PR went in, and QA, pre-prod and prod deployed that afternoon.
>
> The part I care about is what came after. I scanned the whole repo: dozens of ownership resources lack the parameter — most are `future_*` grants where it's harmless — but two in another module are the exact same shape as the one that broke, and haven't fired yet. I flagged them. I'd rather own "here's the next one" than only the one that paged.

</details>
