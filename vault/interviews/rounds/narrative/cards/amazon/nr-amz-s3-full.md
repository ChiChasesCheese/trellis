---
id: nr-amz-s3-full
node: amazon.full
type: qa
step: 3
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：我自己建的每日健康检查 every settled transaction has its Braintree fee 报警，page 了 on-call。我不是 assignee，但把 page 转给了自己，负责根因、postmortem 和加固。
- 问题：先切片，缺失的费用 100% 是新 standard-ACH 路径上的银行账户交易，约 200 个商户、每天约 1000 万美元。追到单笔交易，payment_instrument_sub_kind 是 NULL，而费用品类是 BT_ 拼上 sub-kind，SQL 里拼 NULL 还是 NULL，所以没有品类可匹配，费用静默没生成，也没有任何报错。
- 我做了什么：往回读 promote 流程，发现一个函数有两个重载，最后的 MERGE 调的是没有银行账户分支的那个，把正确值覆盖成了 NULL。有人提议把 ACH 加进检查的排除名单，我写下数字，说明检查是对的、费用是真的丢了，所以不加。队友先落了止血，我写 postmortem（含 e2e 为什么没抓到的四个原因），并做结构修复：合并成带默认参数的单一函数，用 versioned migration 删掉旧签名，加了从 promotion 到费用生成的 e2e 测试。
- 结果：根因在线程里几分钟内给出，双重载的设计被整个移除，新的 e2e 覆盖了这条链路。我说明确：止血 PR 是队友的，我负责根因和加固。
- 为什么这样做 / 学到：无法映射的 instrument 必须 fail loudly，不能什么都不产出；NULL 传播是 SQL 的属性，所以规则要放在接缝上，而不是某个调用点。

<span class="label">英文口述（60–90 秒）</span>

A daily health check I'd built, 'every settled transaction has its Braintree fee', paged the on-call. I forwarded the page to myself and had the root cause in the thread within a few minutes. Scoping showed that a hundred percent of the missing fees were bank-account transactions on the new standard-ACH path: about two hundred merchants, roughly ten million dollars a day. The fee calculation builds the pricing category as 'BT_' concatenated with the payment-instrument sub-kind. For these transactions the sub-kind was NULL, and in SQL concatenating NULL gives NULL, so no category matched and no fee was written, silently, no exception. The reason: one function had two overloads, and the shared final MERGE called the one-argument version, which had no bank-account branch, and overwrote the correct value. There was pressure to add ACH to the check's exclusion list. I put the numbers in writing: the check was right and the fees were really missing. A teammate landed the stopgap first. I owned the root cause, the postmortem, and the hardening: one function with a defaulted parameter, a versioned migration that drops the old signature, and an end-to-end test spanning promotion through fee generation. The rule I pushed: an unmappable instrument must fail loudly, not emit nothing.

<div class="sources"><b>表达 · business English</b><br>• <b><i>fail loudly</i></b> — 出错时大声失败（不要静默）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“An unmappable payment instrument should fail loudly instead of silently producing no fee.”</span><br>• <b><i>silent failure</i></b> — 静默失败<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The worst part was the silent failure: NULL propagated and no error was ever raised.”</span><br>• <b><i>root cause</i></b> — 根因<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I had the root cause in the thread within a few minutes.”</span></div>
