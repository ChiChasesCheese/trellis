---
id: nr-amz-s5-starl
node: amazon.s5
type: qa
step: 2
---
## Q
【S5 · Net Settlement · interchange 数据源切换（技术决策 + 零回归迁移）】STAR-L 提纲（60–90 秒）

## A
**S**

- **Net settlement** 是多季度项目；我 own **费用侧**（不是 epic owner of record）
- 透传费用来自收单方的 **transaction view**，有时在**出款截止后**才填充

**T**

- 我 **owner** 把最大类别 **credit interchange** 切到更早到达的 **settlement view**

**A**

- 比较**两个方案**：更聪明的动态 fallback，或按费用类型的**静态拆分** + toggle
- 选**静态拆分**：fallback 已有粘性状态和三个 CTE；收入路径的数据源应是**事实**
- **Discovery**：全外连接逐字段比，**>99.9%** 一致，差异全部解释
- 用**生产查询本身**做 `count(*)` 跑整天：~**13.7M 行**，差 **0.224%**
- **暗发布**：toggle 默认关 → 预生产 → 生产；**deploy 和 release 分开**

**R**

- 生产流量切换前，一整天 **13.7M 行**验证在 **0.224%** 以内
- 回填 SQL 成了团队的 **CDC 回填模板**

**L**

- **验证和生产用同一条 SQL**，不会验证 A 却发布 B
- 收入路径的数据源是事实，不是运行时决定
