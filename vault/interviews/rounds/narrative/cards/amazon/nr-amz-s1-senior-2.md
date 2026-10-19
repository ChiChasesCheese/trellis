---
id: nr-amz-s1-senior-2
node: amazon.followups
type: qa
step: 3
---
## Q
<p class="title">Amex 结算管线<span class="meta">03 senior 追问</span></p>

*"How would you make adding a seventh record type cheap?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否能看出自己设计里的重复，并给出可扩展的方案。

<span class="label">回答框架</span>

- 先承认现状：六个 procedure 把同一份偏移表重复了六次
- 再说改法：偏移配置表加一个通用的定宽解析，新增记录类型就是加一行配置
- 最后说验证：用同一批历史文件跑新旧解析，结果逐行对得上才切换

<span class="label">为什么这是最佳实践</span>

重复的偏移表意味着每加一种记录就要复制一个 procedure，出错面也跟着翻倍。把差异收敛成数据（配置行），通用逻辑只维护一份，扩展成本和风险都会下降。后来我在 quality-check 框架里正是用了这个模式。切换前用历史文件做新旧比对，是为了让重构本身不引入新的钱的错误。

<div class="sources"><b>表达 · business English</b><br>• <b><i>config-driven</i></b> — 配置驱动<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Next time I would make the parser config-driven so a new record type is one row.”</span><br>• <b><i>regression-test against history</i></b> — 用历史数据做回归比对<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Before switching I would regression-test the generic parser against historical files.”</span></div>
