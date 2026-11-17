---
id: ai-failure-modes-plausible-idioms
node: ai.failure-modes
type: qa
step: 3
---
## Q
读智能体的 diff 时，哪些“顺手写法”看着对、在边界上和合同不一样？为什么公开测试抓不到？

## A
**常见写法在边界上悄悄越界**

- **`\d`**：字符串正则里的 `\d` 默认匹配 Unicode 的所有十进制数字，不只是 `0-9`；
- **`strip()`**：不带参数时剥掉的是所有 Unicode 空白，包括不间断空格；合同只说空格时，范围就超了；
- **`round`**：半入偶，`round(2.5)` 是 2；
- **浮点金额**：`0.1 + 0.2 != 0.3`，金额要用整数分或 `Decimal`；
- **`isinstance(x, int)`**：`True` 也通过；
- **为什么漏**：公开测试用的是普通输入，这些写法在普通输入上全对。这是读 diff 时的检查清单，不是“智能体一定会这么写”的统计。

```python
import re

print(bool(re.fullmatch(r"\d{4}", "١٢٣٤")))    # True：阿拉伯-印度数字
print(repr("  7 ".strip()))               # '7'：不间断空格被剥掉
print(round(0.5), round(1.5), round(2.5))      # 0 2 2
print(0.1 + 0.2 == 0.3)                        # False
print(isinstance(True, int))                   # True
```

<details class="pt"><summary>延伸</summary>

合同要求只认 ASCII 数字时，写 `re.fullmatch(r"[0-9]{4}", s)`，或给正则加 `re.ASCII` 标志。把这五行当成审查时的搜索词：diff 里出现 `\d`、`strip(`、`round(`、`float`，逐处对照合同。

</details>

**知识点：**AI 的典型错误（Failure Modes）
