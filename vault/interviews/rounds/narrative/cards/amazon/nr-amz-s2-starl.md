---
id: nr-amz-s2-starl
node: amazon.outline
type: qa
step: 5
---
## Q
<p class="title">Quality-check 框架<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 团队有**几十张对账表**，每张都有自己**手写的校验 task**
- 每加一张表 = 写、评审、发布一个新 task

<span class="label">T</span>

- 让加检查变便宜
- 让 "is this data safe to read" 成为**硬条件**，而不是 Slack 约定

<span class="label">A</span>

- **配置表**：一行 = 哪个 subject area 跑哪个存储过程、什么 **SLA**（另有日期列、JSON 参数）
- **通用 executor**（`EXECUTE IMMEDIATE`）写标准化 PASS / FAIL / WARNING；**exception handler** 把崩溃变成 FAIL 行
- **状态行**翻成 **Completed** 并复制到 share 层，下游 **JOIN** 它
- 自己**铺开 8 个 subject area**：加检查 = 插一行
- 生产规模下发现**自己的缺陷**：就绪判断按表，~**50** 个坏商户挡住 **35,000**
- 写 **ADR**：四个方案 + 正确性论证 + 容量分析
- 否决 **VARIANT**（关谓词下推）、**flatten**（单元格大小上限）、**新表**（新基础设施）；选**汇总行 + 每商户失败行**，"**strictest wins**"

<span class="label">R</span>

- 框架 + **8 次铺开**在生产
- 商户级就绪：**designed, reviewed, proven in one subject area**
- 更大范围铺开排在 **net settlement 之后**，不说已上线

<span class="label">L</span>

- **粒度**是随规模要重新审视的设计参数
- 修自己的缺陷走正式的 **ADR**
- 设计任何 gate 先问：一个检查失败，**blast radius** 是谁

<div class="sources"><b>表达 · business English</b><br>• <b><i>decouple</i></b> — 解耦<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The status table decouples downstream readers from how each check is implemented.”</span><br>• <b><i>single source of truth</i></b> — 唯一可信的数据源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The replicated status row became the single source of truth for whether data is safe to read.”</span><br>• <b><i>make the right thing the easy thing</i></b> — 让正确的做法成为最省事的做法<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Insert-a-row onboarding made the right thing the easy thing for every subject area.”</span></div>
