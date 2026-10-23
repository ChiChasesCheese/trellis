---
id: hl-sd01-pipeline
node: system-design.sd01-unused-code
type: qa
step: 12
---
## Q
无用代码分析流水线的六个阶段是什么？每阶段产出什么？

## A
固定快照（git 提交 + 构建产物）上：
1. **索引**（并行，按构建目标分片）：Java 读 `.class` 字节码（ASM）+ 调试信息回映射源码行；C++ 用 clang 索引 + 链接器 `--gc-sections` 报告；Python / 脚本轻量解析，低可信度。输出 `defs`、`refs`、`strings`；
2. **汇总**（按 symbol id shuffle）：CSR 图 + 符号表 + 字符串表；
3. **动态证据**（可选，持续收集）：类加载日志 `-Xlog:class+load`，JFR / 方法级覆盖 agent（抽样），按（服务，版本）聚合保留 90 天；
4. **标记**（单机，亚秒到数秒）：`roots = A ∪ B ∪ C ∪ E(弱) ∪ G`，RTA 虚调用解析，lambda / 方法引用边；
5. **分级与见证**：L0–L3 + blockers + 证据；
6. **报告 + 按 owner 拆 PR**（机器人）→ 人审 → 软删除 → 真删 → 回路指标。
