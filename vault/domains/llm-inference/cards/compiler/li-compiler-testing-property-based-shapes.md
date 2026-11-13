---
id: li-compiler-testing-property-based-shapes
node: compiler.testing
type: qa
step: 3
---
## Q
怎样用基于性质的测试（property-based testing，如 Hypothesis）为内核或编译器自动生成形状和输入？它比手写的形状列表强在哪里？

## A
**基于性质的测试：** 不写具体的测试用例，而是描述"输入的范围"和"输出必须满足的性质"，由测试框架随机生成大量输入去检验；一旦找到失败的输入，框架会自动缩减它，给出最简单的反例。Python 里常用的库是 Hypothesis。

**为内核生成形状：**

```python
import torch
from hypothesis import given, settings, strategies as st

dims = st.integers(min_value=1, max_value=8192)

@settings(max_examples=300, deadline=None)
@given(m=dims, n=st.sampled_from([64, 128, 4096, 4095, 11008]), scale=st.sampled_from([1e-3, 1.0, 100.0]))
def test_softmax_properties(m, n, scale):
    x = torch.randn(m, n, device="cuda", dtype=torch.bfloat16) * scale
    y = my_softmax(x).float()                                   # 被测内核
    assert torch.isfinite(y).all()                              # 性质 1：没有 inf/NaN
    assert torch.allclose(y.sum(-1), torch.ones(m, device="cuda"), atol=2e-2)   # 性质 2：每行和为 1
    torch.testing.assert_close(y, torch.softmax(x.double(), -1).float(), rtol=2e-2, atol=2e-3)
```

**可以检验的性质：**
- **和参考实现一致**（最强的性质）。
- **数学不变量：** softmax 每行和为 1、所有值在 0 到 1 之间；归一化后每行的均方根约为 1；矩阵乘以单位矩阵等于自己。
- **蜕变关系：** 输入整体加一个常数，softmax 输出不变；批拆成两半分别算再拼接，等于整批计算的结果。
- **不崩溃：** 对合法输入不报错、不产生 NaN。

**比手写形状列表强在哪里：**
- **覆盖意想不到的组合：** 手写列表反映的是写测试的人想到的情况；随机生成会碰到 `m = 1, n = 4095` 这类组合。
- **自动缩减：** 发现 `m = 3817, n = 11008` 失败后，Hypothesis 会尝试缩小，可能告诉你 `m = 1, n = 4095` 就能复现，直接指向边界处理问题。
- **可复现：** 失败的例子会被记录在本地数据库，下次运行优先重试，修复后自动变成回归测试。

**实践注意：**
- GPU 测试较慢，`max_examples` 适中，在夜间任务中加大。
- `deadline=None` 关闭单例超时，避免首次编译导致误报。
- 把找到的反例显式加进固定的参数化列表，防止以后随机生成碰不到。
