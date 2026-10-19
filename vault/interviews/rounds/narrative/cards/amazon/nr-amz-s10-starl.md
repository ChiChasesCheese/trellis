---
id: nr-amz-s10-starl
node: amazon.outline
type: qa
step: 29
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 一家大型电商商户切到 **net settlement**
- 部分**退款费**带着旧的 **monthly** billing terms

<span class="label">T</span>

- 我 own **爆炸半径估算**和**根因**
- 修复范围必须按**正确的数字**，不能按错谓词

<span class="label">A</span>

- 写估算查询：**约 20 万行费用、六十个商户**
- **没人行动之前**重读自己的谓词，发现**错了**
- 它没检查新计划在**费用创建时已存在**；很多是**几个月后回填**的，写入时是对的
- **加上该条件**重跑，真实范围小得多
- **根因**：退款费路径**复制了 credit 的历史计划 ID**，没有在费用创建时重新解析
- 另发现**上游脆弱点**：计划在 stream 给当天 credit 盖章**一个半小时之后**才写入

<span class="label">R</span>

- 真实范围：**~22K 行、30 商户、不到 $6K**，而不是 200K 和 60
- **一个修法同时覆盖**两个脆弱点：费用创建时解析生效计划

<span class="label">L</span>

- 宁可**公开撤回自己的数字**，也不按错谓词定补救范围
- 每个结论配一条**可重跑的查询**；爆炸半径谓词必须检查**时间有效性**

<div class="sources"><b>表达 · business English</b><br>• <b><i>own up to a mistake</i></b> — 主动承认错误<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I owned up to the mistake in public instead of letting the number stand.”</span><br>• <b><i>rerun the numbers</i></b> — 重新跑数<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I reran the numbers with a time-validity condition.”</span><br>• <b><i>close both gaps</i></b> — 把两个缺口一起补上<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“One fix at fee creation closes both gaps.”</span></div>
