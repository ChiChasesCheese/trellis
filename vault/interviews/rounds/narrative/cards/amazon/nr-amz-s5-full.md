---
id: nr-amz-s5-full
node: amazon.full
type: qa
step: 5
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：Net Settlement 是多季度项目，我负责其中的费用侧。透传费用（interchange、scheme、chargeback）都来自收单方的 transaction view，而这个视图有时在当天出款截止之后才填好，所以费用赶不上净额结算窗口。
- 决定：我负责把最大的一类，信用卡 interchange，切到更早到达的 settlement view。有两条路：把现有的“哪个视图有数就用哪个”fallback 做得更聪明，或者按费用类型静态拆分并用 toggle 控制。我选了静态拆分，因为 fallback 已经长出粘性状态和三个 CTE，而收入路径上的数据源应该是事实，不是运行时的判断。
- 验证：先做 discovery，用 FULL OUTER JOIN 加 EQUAL_NULL 逐字段比对，一致率超过 99.9%，0.07% 的不匹配全是只在一侧当天才有的记录（时序问题），两个差异（FEE_SEQUENCE_CODE、ALT_DISPUTE_ID）都能解释。然后把即将上线的生产查询本身改成 count(*) 跑一整天，约 1373 万行，差 0.224%（多 30,760 行）。因为验证和生产用同一条 SQL，所以不会验证的是 A、发布的是 B。
- 发布：toggle 默认关，先在预生产打开，再到生产，deploy 和 release 分成两步。旧 task 在 toggle 打开时显式排除 interchange，两个 task 互补，不会重复计费。
- 结果与学到：切换前一整天 1373 万行的验证在 0.224% 以内；回填 SQL 成了团队做 CDC 回填的模板。收入路径的数据源要是事实；验证和上线用同一条 SQL。

<span class="label">英文口述（60–90 秒）</span>

Our pass-through fees, interchange, scheme, chargeback, all came from the acquirer's transaction view, and that view sometimes wasn't populated until after the daily payout cutoff, so fees missed the net-settlement window. I owned switching the biggest category, credit interchange, to the settlement view, which arrives earlier. I had two options: make the existing fallback smarter, or split statically by fee type behind a feature toggle. I chose the static split, because the fallback had already grown sticky state and three CTEs, and in a revenue path I want the source of truth to be a fact, not a runtime decision. Before switching I ran a discovery comparison, a full outer join field by field, with over ninety-nine point nine percent parity and every difference explained. Then I ran the production query itself as a count(*) over a full day: about 13.7 million rows, within 0.224 percent. Validation and production share the same SQL, so I can't validate one thing and ship another. I shipped it dark, toggle off, enabled in pre-prod, then production, because deploy and release are two separate steps. The backfill SQL became the team's template for CDC backfills.

<div class="sources"><b>表达 · business English</b><br>• <b><i>cut over</i></b> — 切换（到新系统 / 新数据源）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We only cut over once the new source matched the old one.”</span><br>• <b><i>parallel run</i></b> — 新旧并行跑、逐项对比<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Comparing old and new outputs side by side is how you earn a zero-regression cutover.”</span><br>• <b><i>zero-regression migration</i></b> — 零回归迁移<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The bar was a zero-regression migration: every fee had to match.”</span></div>
