---
id: hl-sd01-roots-e-g-weak
node: system-design.sd01-unused-code
type: qa
step: 11
---
## Q
根的 E–G 三类是什么？字符串命中怎么当「弱根」，它借鉴了什么工具的思想？

## A
- **E 配置里的类名**：YAML / JSON / properties / XML 中出现的 FQN 字符串；
- **F 测试**：单独作为一类根，测试作根与不作根各跑一次，得到「仅测试使用」；
- **G 显式保留**：`@KeepAlive("disaster-recovery")` / 允许名单（owner 声明）。

**字符串命中（弱根）**：索引时收集字节码常量池里的所有字符串常量，以及仓库所有文本文件（配置、脚本、文档）里形如 FQN 的 token，和符号表匹配。命中 → 标为弱根：不直接保活，但**降低可信度**并作为 blocker 写进证据。这是 ProGuard / R8 的 `-keep` 规则思想：保守地保护动态使用的东西。

根集合错一个，要么大量误报（把活代码判死，危险），要么大量漏报。
