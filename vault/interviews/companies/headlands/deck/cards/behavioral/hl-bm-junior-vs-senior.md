---
id: hl-bm-junior-vs-senior
node: behavioral.method
type: qa
step: 15
---
## Q
"最难的 bug" 的 junior 版回答为什么不够？和 senior 版相比，senior 版多了哪五样东西？

## A
Junior 版：*"A health check alerted that some transactions had no fee. I found a NULL in a field, fixed the function, and we added a test."* —— 缺**定位方法、为什么没报错、测试为什么漏、规则**。

Senior 版（约 184 词、约 75 秒）多了：
1. **方法**：切片（slice）→ 单行 → 回溯（walk back）。
2. **机制**：NULL 拼接仍是 NULL，所以什么都匹配不上也不报错；函数有两个重载，最终 `MERGE` 调用了没有该支付类型分支的那个。
3. **测试复盘**：四个端到端测试漏掉它的原因。
4. **边界**：用对照组和年龄分桶排除"只是晚到"；拒绝把该类型加进检查的排除名单。
5. **规则**：无法映射的输入必须大声失败（fail loudly）。
