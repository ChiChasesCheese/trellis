---
id: review-ai-hallucinated-api
node: review.ai-code
type: qa
step: 1
---
## Q
评审 AI 生成的 diff，里面调用了 `itertools.batched`、`dict.get_or_default`、`str.contains`。测试环境跑过了，你还需要核实什么？

## A
**AI 会写出看着合理却不存在的 API，或存在但版本不对的 API：逐个核实**

- **不存在的名字**：模型按“应该有这样的函数”来写，`dict.get_or_default`、`list.push`、`str.contains` 在 Python 里都没有；
- **版本不对**：`itertools.batched` 从 Python 3.12 才有，3.11 上直接 `AttributeError`；测试环境和生产版本不同，就会在上线后才爆；
- **签名对不上**：参数名、顺序、返回类型凭印象写，比如返回迭代器却被当列表用；
- **核实的办法**：查官方文档的“版本变更”说明；在目标版本的解释器里 `hasattr` / `help()` 一下；类型检查器（mypy、pyright）会指出不存在的属性；
- **项目里的约定函数同样**：AI 可能调用你仓库里并不存在的 helper，grep 一下名字。

```python
import itertools, sys

print(sys.version_info[:2])
for name in ("batched", "pairwise", "chunked"):
    print(name, hasattr(itertools, name))
# 3.11：batched False（3.12 才加入），pairwise True（3.10 起），chunked False（不存在，来自第三方 more-itertools）

print(hasattr({}, "get_or_default"), hasattr("", "contains"))     # False False
```

**知识点：**评审 AI 生成的代码（Reviewing AI Code）
