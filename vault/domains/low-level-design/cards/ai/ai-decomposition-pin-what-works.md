---
id: ai-decomposition-pin-what-works
node: ai.decomposition
type: qa
step: 4
---
## Q
起始代码已经把几件事做对了（比如拒绝 `True`、字符串、`None`）。修别的缺陷之前，为什么要先给这些行为各写一个测试？

## A
**已经对的行为也要先钉住**

- **没人守着的正确行为最容易被改坏**：修缺陷、重构校验函数时，智能体可能顺手换一种写法，行为变了而公开测试根本不测；
- **做法**：在改动前跑一遍，对已经通过的规则也写测试并保留，它们一开始就是绿的；
- **和红测试不同**：红测试驱动修复，绿测试防止回归，两种都要有；
- **之后**：任何改动之后全量跑，这批绿测试变红，就是你改坏了它。

```python
def valid_score_old(x): return type(x) is int and 0 < x <= 5
def valid_score_new(x): return isinstance(x, int) and 0 < x <= 5    # “顺手重构”

PINNED = [(True, False), ("3", False), (None, False), (3, True)]
for f in (valid_score_old, valid_score_new):
    broken = [x for x, want in PINNED if f(x) != want]
    print(f.__name__, broken)
# valid_score_old []
# valid_score_new [True]
```

**知识点：**拆成可验证的小步（Decomposition）
