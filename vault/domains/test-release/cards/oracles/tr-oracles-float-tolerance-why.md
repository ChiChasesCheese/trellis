---
id: tr-oracles-float-tolerance-why
node: oracles.float-tolerance
type: qa
step: 1
---
## Q
测试浮点结果为什么不能用 `==`？绝对容差（atol）和相对容差（rtol）分别解决什么问题，为什么通常要组合使用？

## A
**为什么不能用 `==`**：浮点数只有有限位，几乎每次运算都要舍入；运算顺序一变，舍入就不同。`0.1 + 0.2 == 0.3` 是 `False`；同样的求和换一种并行拆分，最后几位也会变。正确的实现也会产生不同的位，所以 `==` 会让测试随机失败。

**绝对容差**：`|actual − expected| ≤ atol`。
- 适合期望值接近 0 的情况。
- 问题：对大数没意义。期望值是 1e6 时，1e-5 的绝对容差比浮点本身的精度还小，正确结果也会失败；期望值是 1e-8 时，1e-5 的绝对容差又大到什么都能通过。

**相对容差**：`|actual − expected| ≤ rtol × |expected|`。
- 按数值大小缩放，适合跨数量级的数据。
- 问题：期望值是 0 或接近 0 时，右边趋近 0，任何微小误差都失败。而神经网络、物理计算的结果里经常有本该是 0 的值，算出来是 1e-9。

**组合**：`|actual − expected| ≤ atol + rtol × |expected|`。大数靠相对项，接近 0 时靠绝对项兜底。这正是 `numpy.allclose` 和 `torch.testing.assert_close` 使用的公式。

**例**：`rtol=1e-5, atol=1e-8`：期望 1000.0 时允许误差约 0.01；期望 0.0 时允许误差 1e-8。

**注意不对称**：公式只用 `expected` 的绝对值缩放，所以 `allclose(a, b)` 和 `allclose(b, a)` 结果可能不同；参数顺序要固定为"实际、期望"。Python 的 `math.isclose` 则用两者中较大的绝对值，是对称的。
