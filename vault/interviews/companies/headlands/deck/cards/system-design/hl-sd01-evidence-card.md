---
id: hl-sd01-evidence-card
node: system-design.sd01-unused-code
type: qa
step: 17
---
## Q
一个无用代码候选的「证据卡」包含哪些字段？活的和死的符号各怎么解释？可信度怎么给？

## A
证据卡字段：symbol、level（L0–L3）、confidence、snapshot（提交 + 构建号）、**witness**（考虑了多少个根、入边的引用者及它们是否也不可达、死簇范围如 3 类 / 412 LOC）、signals（生产类加载日志 90 天 312 个 JVM 实例从未加载、最后一次修改时间及 owner、最后一次出现活引用的提交）、blockers（无字符串命中、非导出、无反射注解）、suggested（按簇的软删除 PR）。

各自的解释依据：
- **活的符号**：见证 = 从某个根到它的**最短路径**（BFS 时记录 parent 指针）；
- **死的符号**：见证 = 「所有入边的引用者本身都不可达」+ 死簇范围，再加 blockers 清单。

可信度由**可审计规则**给出，不是黑盒打分：L0 / L1 且 90 天未被加载 = HIGH；L1 但有弱根（字符串命中）= MEDIUM；L2 = 需额外检查；L3 = 仅提示，永不自动。
