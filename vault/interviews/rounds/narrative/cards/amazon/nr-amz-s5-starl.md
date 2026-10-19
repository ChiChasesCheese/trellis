---
id: nr-amz-s5-starl
node: amazon.outline
type: qa
step: 14
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- **Net settlement** 是多季度项目；我 own **费用侧**（不是 epic owner of record）
- 透传费用来自收单方的 **transaction view**，有时在**出款截止后**才填充

<span class="label">T</span>

- 我 **owner** 把最大类别 **credit interchange** 切到更早到达的 **settlement view**

<span class="label">A</span>

- 比较**两个方案**：更聪明的动态 fallback，或按费用类型的**静态拆分** + toggle
- 选**静态拆分**：fallback 已有粘性状态和三个 CTE；收入路径的数据源应是**事实**
- **Discovery**：全外连接逐字段比，**>99.9%** 一致，差异全部解释
- 用**生产查询本身**做 `count(*)` 跑整天：~**13.7M 行**，差 **0.224%**
- **暗发布**：toggle 默认关 → 预生产 → 生产；**deploy 和 release 分开**

<span class="label">R</span>

- 生产流量切换前，一整天 **13.7M 行**验证在 **0.224%** 以内
- 回填 SQL 成了团队的 **CDC 回填模板**

<span class="label">L</span>

- **验证和生产用同一条 SQL**，不会验证 A 却发布 B
- 收入路径的数据源是事实，不是运行时决定

<div class="sources"><b>表达 · business English</b><br>• <b><i>ship it dark</i></b> — 先暗发布：代码上线但功能默认关<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I shipped it dark, with the toggle off, and enabled it in pre-prod first.”</span><br>• <b><i>deploy is not release</i></b> — 部署不等于放量：上线代码和打开功能是两步<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Deploy is not release, so we could roll back by flipping a toggle.”</span><br>• <b><i>static split</i></b> — 静态拆分，职责在设计时就固定<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I chose a static split by fee type over a smarter runtime fallback.”</span></div>
