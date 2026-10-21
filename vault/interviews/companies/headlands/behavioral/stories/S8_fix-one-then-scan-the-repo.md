# S8 · 修一个，再扫整个仓库找下一个（好奇心 · 消灭一类问题 · 收窄自己说宽的话）

- 用于：curiosity / debug under pressure / low ego / how do you prevent recurrence。

**Hook：「I'd rather own 'here's the next one' than just the one that paged.」**

## 数字

- 7 分钟出根因；QA → pre-prod → prod 当天部署。
- 事后扫描：79 个同类资源，42 个缺该参数；多数是无害的 `future_*`，2 个在别的模块、形状相同、尚未触发。

## 60 秒

**S**
- An **infra-repo release** failed in **QA**: Snowflake **rejected** `GRANT OWNERSHIP` because another role held a **dependent grant**.
- Someone else was named; I was **cc'd**.

**T**
- **Unblock** the release.

**A**
1. In **7 minutes** I posted the **root cause**: no `outbound_privileges`, so Terraform never **revoked** the dependents.
2. Posted the **fix**, `outbound_privileges = "REVOKE"`, and a **check of neighboring modules**.
3. Asked **permission**, pushed the **PR**; **three environments** deployed that day.
4. **Afterwards** I scanned the **whole repo**: **42 of 79** similar resources lacked it.
5. Most were **harmless future grants**; **two** in another module had the **same shape** and hadn't fired. I **flagged** them.

**R**
- Same-day unblock; the **next failure** named **before it fired**.

**L**
- **Fixing this one** and **eliminating the class** are different jobs; keep claims **as narrow as what I checked**.

## 2 分钟（在 60 秒上加）

- **Mechanism**: ownership transfer needs dependents revoked first; the resource expresses that with `outbound_privileges` (**REVOKE** or **COPY**); unset, apply **fails**.
- **Terraform has no transactions**: a failed apply leaves **partial state**; keep dangerous changes **small and re-runnable**.
- **Corrected claim**: I had once said it was the only such resource; the scan **proved that false**. The true version: "I checked neighboring modules that day; afterwards I found dozens, mostly harmless, and two real ones."

## 追问

- **Why were future grants harmless?** They have **no existing dependents** to conflict with. 【待补：你核实的依据】
- **How did you scan?** 【待补：方法（grep / 脚本 / state）】
- **Most dangerous "harmless" Terraform operation?** **Renaming** a resource: default is **delete and recreate**; use a `moved` block or `state mv`.
- **Why not fix the other module yourself?** Not my module, and they hadn't fired; **flag with evidence**, let the **owner** decide.

## 别说

- "the only resource in the repo missing it"；"我被指派调查"（我只是被 cc）。
- 把 7 分钟当炫耀。

## 待补

- 【待补：那两个资源后来有没有被修】
