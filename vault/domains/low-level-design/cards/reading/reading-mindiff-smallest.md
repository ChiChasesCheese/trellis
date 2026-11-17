---
id: reading-mindiff-smallest
node: reading.minimal-diff
type: qa
step: 1
---
## Q
一个运费函数对 `pro` 套餐之外都多收了 1 元，你在同一个函数里顺手改了变量名、换成了三元表达式、调整了缩进。为什么评审的人会不高兴？怎么衡量一个改动“够小”？

## A
**diff 里每一行都应该能回答“为什么要改它”；顺手的整理另开一个提交**

- **评审的成本和 diff 行数成正比**：一行修复淹没在六行改写里，评审的人得逐行确认“这些改写有没有改变行为”；
- **越小越容易回退**：线上出问题时，一行改动可以精确地撤销，整段重写不行；
- **风格整理会掩盖真正的改动**：`git blame` 之后看到的都是你，之前的上下文丢了；
- **整理没有错，只是要分开**：先提交修复，再提交纯重构（行为不变），或者反过来，一次提交只做一件事；
- **度量**：用 `git diff --stat` 看，改动的行里有多少是“修缺陷所必需的”。

```python
import difflib

old = ['def rate(kind):\n', '    if kind == "pro":\n', '        return 9\n', '    return 5\n']
minimal = old[:3] + ['    return 6\n']                                   # 只改要改的一行
noisy = ['def rate(plan):\n', '    return 9 if plan == "pro" else 6\n']   # 顺手重写

def changed(a, b):
    return sum(l[0] in "+-" and not l.startswith(("+++", "---"))
               for l in difflib.unified_diff(a, b))

print(changed(old, minimal), changed(old, noisy))                         # 2 6
```

**知识点：**最小改动（Minimal Diff）
