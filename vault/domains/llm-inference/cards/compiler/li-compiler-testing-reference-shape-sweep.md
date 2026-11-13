---
id: li-compiler-testing-reference-shape-sweep
node: compiler.testing
type: qa
step: 1
---
## Q
怎样系统地测试一个算子或内核（kernel）的数值正确性？写出一个按形状和数据类型扫描、和参考实现对比的 pytest 测试。

## A
**内核：** 在加速器上执行的一个计算函数，比如自定义的 RMSNorm、矩阵乘法、注意力。**参考实现：** 用最直白的方式写的、被信任的实现，通常是 PyTorch 的逐步计算，在更高精度（FP32 或 FP64）下运行。

```python
import pytest, torch

SHAPES = [(1, 1), (1, 4096), (7, 4096), (16, 4096), (17, 4095), (2048, 8192), (1, 131072)]
DTYPES = {torch.float32: (1.3e-6, 1e-5), torch.bfloat16: (2e-2, 2e-2), torch.float16: (2e-3, 2e-3)}

def ref_rmsnorm(x, w, eps=1e-6):
    x32 = x.double()                                   # 参考在 FP64 下计算
    return (x32 * torch.rsqrt(x32.pow(2).mean(-1, keepdim=True) + eps) * w.double())

@pytest.mark.parametrize("shape", SHAPES)
@pytest.mark.parametrize("dtype", DTYPES)
def test_rmsnorm(shape, dtype):
    torch.manual_seed(0)
    x = torch.randn(shape, device="cuda", dtype=dtype) * 3
    w = torch.randn(shape[-1], device="cuda", dtype=dtype)
    out = my_rmsnorm(x, w)                             # 被测内核
    rtol, atol = DTYPES[dtype]
    torch.testing.assert_close(out.double(), ref_rmsnorm(x, w), rtol=rtol, atol=atol)
```

**形状怎么选：**
- **最小值：** 1（单个 token、单个元素）。
- **块大小的倍数和 ±1：** 内核按块处理，边界块最容易出错，如 16、17、4,095、4,096。
- **质数和奇数：** 如 7、4,093。
- **生产中的真实形状：** 模型的隐藏宽度、头维度、词表大小。
- **极大值：** 很长的归约维度（如 131,072），能暴露累加精度问题。

**数据类型和数值范围：**
- 每种支持的类型都测，容差按类型分别设定。
- 输入分布不只用标准正态：加上很大的值（放大 100 倍）、很小的值、全零、含 inf/NaN（检查是否按预期传播）。

**内存布局：** 连续张量、转置后的张量、切片得到的非连续张量、非对齐的起始地址。

**容差的依据：** 先让参考实现在低精度下运行，和自己的 FP64 结果比较，测出"正确实现在这个精度下的误差"，再把被测内核的容差设在它的若干倍。
