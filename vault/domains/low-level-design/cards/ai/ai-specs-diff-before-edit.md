---
id: ai-specs-diff-before-edit
node: ai.specs
type: qa
step: 3
---
## Q
接到一个修复型的项目：合同十条，现有代码有若干缺陷。为什么第一句话是“先列代码与规则的差异，不要改代码”？列出来的差异怎么用？

## A
**先出差异清单，再决定改什么**

- **读多于写**：只读不改，智能体不会把几处缺陷混在一个改动里，你也有机会先纠正它的理解；
- **对账**：它的清单和你自己读出的缺陷对一遍，对不上的地方就是理解分歧，先谈清；
- **转成测试**：清单里每一项变成一个会失败的测试，这是下一步的输入；
- **做法本身可运行**：把每条规则写成函数，对现有代码跑一遍，失败的就是差异。

```python
def top_titles(scores, n):                       # 现有代码
    return sorted(scores, key=scores.get)[:n]

RULES = {
    "最高分在前": lambda f: f({"a": 1, "b": 3}, 1) == ["b"],
    "同分按 id 升序": lambda f: f({"b": 2, "a": 2}, 2) == ["a", "b"],
    "n 最多 50": lambda f: len(f({str(i): i for i in range(60)}, 99)) == 50,
    "n 为 0 返回空": lambda f: f({"a": 1}, 0) == [],
}
print([name for name, ok in RULES.items() if not ok(top_titles)])
# ['最高分在前', '同分按 id 升序', 'n 最多 50']
```

**知识点：**写清任务（Specifying the Task）
