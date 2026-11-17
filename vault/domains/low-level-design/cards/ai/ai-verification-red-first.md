---
id: ai-verification-red-first
node: ai.verification
type: qa
step: 5
---
## Q
合同里的示例在修复前的旧代码上也能通过。这样的测试能证明修复有效吗？每个缺陷现象应该怎么留测试？

## A
**每个现象一个在旧代码上变红的测试**

- **示例分不出新旧**：旧代码也过的测试，对“修好了没有”没有任何信息；
- **先红再绿**：写完测试先在旧代码上跑，必须失败，而且失败的原因正是你要修的那个缺陷；
- **逐个现象**：投诉里有几个现象就留几个测试，修完一个才进下一个；
- **留下来**：修复之后这个测试保留，它就是防回归的那一条。

```python
from datetime import date

def old(d: date) -> bool:
    return d.weekday() > 5       # 缺陷：周六（5）被漏掉

def new(d: date) -> bool:
    return d.weekday() >= 5      # 合同：周末是周六和周日

example = date(2026, 11, 22)     # 合同示例用的是周日
saturday = date(2026, 11, 21)
print(old(example), new(example))      # True True：示例分不出新旧
print(old(saturday), new(saturday))    # False True：这条在旧代码上红
```

**知识点：**验证输出（Verification）
