---
id: li-numerics-formats-tolerances-by-dtype
node: numerics.formats
type: qa
step: 5
---
## Q
测试中比较两个张量时，`rtol` 和 `atol` 应该按数据类型怎样设？`torch.testing.assert_close` 的默认容差是多少？为什么不能对所有类型用同一个容差？

## A
**判定公式：** `torch.testing.assert_close(actual, expected, rtol=, atol=)` 要求每个元素满足：

`|actual − expected| ≤ atol + rtol × |expected|`

- **rtol（相对容差）：** 允许的误差和数值大小成比例，用于普通大小的数。
- **atol（绝对容差）：** 允许一个固定的误差下限，用于接近 0 的数（此时相对误差没有意义）。

**`torch.testing.assert_close` 不指定时的默认值：**

| 数据类型 | rtol | atol |
|---|---|---|
| float64 | 1e-7 | 1e-7 |
| float32 | 1.3e-6 | 1e-5 |
| float16 | 1e-3 | 1e-5 |
| bfloat16 | 1.6e-2 | 1e-5 |

规律：rtol 约等于该格式的机器 epsilon（1 附近相邻可表示数的间隔）的量级。BF16 的 epsilon 是 7.8×10⁻³，所以单次舍入的相对误差就在 10⁻³ 到 10⁻² 之间。

**为什么不能统一：** 用 float32 的容差检查 bfloat16 的结果，单次舍入就会失败，测试全红；反过来用 bfloat16 的容差检查 float32，真正的实现错误（比如差了 0.5%）也能通过。

**更大计算链的容差：** 默认值适合"一次运算"的比较。经过一个 4,096 维矩阵乘法、或者几十层模型之后，误差会累积：
- **按理论放大：** 长度为 K 的求和，误差的量级大致随 √K 增长。
- **按经验校准：** 用高精度参考（FP32 甚至 FP64）对同一输入算一遍，再让"已知正确的"低精度实现也算一遍，测出它们之间的误差分布，把阈值设在这个分布的上沿再留余量。

**实践建议：**
- 比较时先都转成 float32：`assert_close(a.float(), b.float(), ...)`，避免比较过程本身引入舍入。
- 除了逐元素容差，再看汇总指标：最大绝对误差出现在哪个位置、余弦相似度、误差超标的元素比例。只有极少数元素超标、且都在接近 0 的位置，通常是 atol 设得太小，而不是实现错误。
