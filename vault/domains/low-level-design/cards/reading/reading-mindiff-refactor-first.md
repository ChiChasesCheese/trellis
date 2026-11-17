---
id: reading-mindiff-refactor-first
node: reading.minimal-diff
type: qa
step: 4
---
## Q
价格格式化的代码在三个地方各复制了一份，现在要加“币种符号”。是直接改三处，还是先重构？怎么判断，怎么做才安全？

## A
**先让改动变容易，再做改动：重构单独提交，行为保持不变**

- **判断标准**：新功能要在 N 处重复的地方都改一遍，并且容易漏一处时，先把重复抽成一处；只改一处就够的，不要重构；
- **顺序**：先写测试钉住现有行为，再做纯重构（输出不变），测试保持绿；最后才加新功能，这时只改一处；
- **两个提交，不要混在一起**：第一个提交评审的人只需要确认“行为没变”；第二个提交只有新功能；
- **重构范围只到“新功能需要”为止**：不顺带整理别的；
- **没有测试、赶时间、代码快废弃**：不重构，直接做最小的改动，在评审说明里讲清风险。

```python
# 提交 1：纯重构，三处调用换成同一个函数；输出不变
def money(cents): return f"{cents / 100:.2f}"

def invoice_line(c): return "invoice " + money(c)
def email_line(c): return "email " + money(c)
def report_line(c): return "report " + money(c)

assert invoice_line(1234) == "invoice 12.34"          # 钉住的旧行为
# 提交 2：新功能只改一处
def money(cents, symbol="$"): return f"{symbol}{cents / 100:.2f}"
print(invoice_line(1234), email_line(5), report_line(99))   # 三处同时带上符号
```

**知识点：**最小改动（Minimal Diff）
