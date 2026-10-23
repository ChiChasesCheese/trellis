---
id: hl-bq-q14-hardest-bug
node: behavioral.question-bank
type: qa
step: 29
---
## Q
讲一个你调试过的最难的 bug。（75 秒）
Hardest bug you've debugged.

## A
故事：S3（备选：S8 的 Terraform 7 分钟 RCA）。

- **No error, just missing rows**：我建的**每日检查**发现已结算交易**没有手续费**，约 **200 个商户**。
- **Method**：**切片（slice）→ 单行 → 回溯**；原因是 **NULL 拼接** 加上最终 `MERGE` 选错的**函数重载**。
- **Tests and fix**：测试漏掉它的**四个原因**；合并成**一个函数**、**版本化 `DROP`**、新的**端到端测试**；规则：**fail loudly**。
