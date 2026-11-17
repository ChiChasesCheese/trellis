---
id: api-specs-gaps-ask
node: api.specs
type: qa
step: 4
---
## Q
需求或面试题对某个输入（比如传入 `None` 的配置）只字未提。该直接选一种处理往下写，还是先问？选了之后怎么留下痕迹？

## A
**规格留白的地方：先问，问不到就写下决定**

- **留白的代价**：你按一种理解写，测试按另一种理解测，错在一处，整条用例红；
- **先问**：一句话列出选项和你的默认，例如“`None` 我按 400 处理，可以吗？”，一分钟的事；
- **问不到**：选最保守的（拒绝，不要猜着容忍），把决定写进 docstring 的 Decisions，每条各配一个测试；
- **不要**：把实现的副作用当规格，下次改实现就破坏了兼容。

```python
class Blocklist:
    """Requires: words is a list of str.
    Decision (spec is silent): None or any non-iterable -> ValueError.
    Decision: matching is case-sensitive substring, not regex, not whole word."""
    def __init__(self, words):
        if isinstance(words, (str, bytes)) or not hasattr(words, "__iter__"):
            raise ValueError("words must be a list")
        self.words = tuple(words)

print(Blocklist(["spam"]).words)
```

**知识点：**规格与契约（Specifications）
