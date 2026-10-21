---
id: nr-amz-s5-senior-3
node: amazon.followups
type: qa
step: 24
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">03 senior 追问</span></p>

*"Why a static split instead of improving the dynamic fallback, and when would the dynamic one have been the right call?"*

## A
<span class="label">面试官在探</span> 面试官在探：你做技术取舍时能不能说清条件，而不是只讲结论。

<span class="label">回答框架</span>

- 先说收入路径要求可预测：同一输入永远走同一来源，出错时能一眼看出是哪边
- 再说 fallback 的代价：粘性状态、三个 CTE，调试要还原运行时当时选了哪个视图
- 承认动态方案适合的场景：来源真的不稳定且没有谁更权威
- 最后说我怎么确认两个来源可互换：用 discovery 的数据说话

<span class="label">为什么这是最佳实践</span>

静态拆分把复杂度从运行时挪到设计时：设计时的决定可以评审、可以测试，运行时的决定只能事后复盘。只有当两个来源都不权威、且延迟不可预测时动态选择才值得，而这里 settlement view 更早到达且数据一致，就没有理由保留动态逻辑。

<div class="sources"><b>表达 · business English</b><br>• <b><i>move complexity to design time</i></b> — 把复杂度从运行时挪到设计时<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The static split moves complexity to design time, where it can be reviewed and tested.”</span><br>• <b><i>debuggability</i></b> — 可调试性<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Debuggability mattered, because with a sticky fallback you had to reconstruct which view it picked.”</span></div>
