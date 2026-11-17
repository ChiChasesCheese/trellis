---
id: review-ai-mirror-tests
node: review.ai-code
type: qa
step: 4
---
## Q
AI 一并写了测试，覆盖率 100%，全绿。为什么这些测试可能什么都没验证？怎么检验？

## A
**测试如果复述了实现，实现错了它跟着错：用“故意改坏”检验测试**

- **复述实现**：测试里重新计算一遍同样的公式、断言返回值等于函数自己返回的值，实现有错，测试跟着对；
- **模拟得过多**：把所有依赖都 mock 掉，最后只验证了“mock 被调用了”；
- **只测快乐路径**：没有边界、没有失败路径；
- **检验方法（变异测试的手工版）**：把实现里的 `<` 改成 `<=`、`+` 改成 `-`，测试该变红；不变红的测试不防任何东西；
- **期望值手写自规格**：用具体的数字（100 的 9 折是 90），不是用公式算出来的数。

```python
def discount(amount, rate=0.9):
    return amount * (1 - rate)                    # 缺陷：应该是 amount * rate

def test_mirror():                                # AI 写的：复述了同一个公式
    assert discount(100) == 100 * (1 - 0.9)

def test_spec():                                  # 手写：规格里 100 的 9 折是 90
    assert discount(100) == 90

for t in (test_mirror, test_spec):
    try: t(); print(t.__name__, "绿")
    except AssertionError: print(t.__name__, "红")     # test_mirror 绿 / test_spec 红
```

**知识点：**评审 AI 生成的代码（Reviewing AI Code）
