---
id: tr-oracles-float-tolerance-api-defaults
node: oracles.float-tolerance
type: qa
step: 2
---
## Q
`numpy.allclose`、`numpy.testing.assert_allclose`、`math.isclose` 和 `torch.testing.assert_close` 的默认容差各是多少？有哪些容易踩的坑？

## A
- **`numpy.allclose(a, b)`**：默认 `rtol=1e-05, atol=1e-08`，判据 `|a − b| ≤ atol + rtol × |b|`，`b` 被当作参考。只返回 `True/False`，失败时不告诉你哪里差。
- **`numpy.testing.assert_allclose(actual, desired)`**：默认 `rtol=1e-07, atol=0`。**默认没有绝对容差**，期望值为 0 时任何非零误差都失败。失败时打印不匹配的元素个数和最大误差，测试里应当用它而不是 `assert np.allclose(...)`。
- **`math.isclose(a, b)`**：默认 `rel_tol=1e-09, abs_tol=0.0`，判据 `|a − b| ≤ max(rel_tol × max(|a|, |b|), abs_tol)`，对称；只比较单个数。和 0 比较时必须显式给 `abs_tol`。
- **`torch.testing.assert_close(actual, expected)`**：不指定时按数据类型选默认值：

| 数据类型 | rtol | atol |
|---|---|---|
| float64 | 1e-7 | 1e-7 |
| float32 | 1.3e-6 | 1e-5 |
| float16 | 1e-3 | 1e-5 |
| bfloat16 | 1.6e-2 | 1e-5 |

判据 `|actual − expected| ≤ atol + rtol × |expected|`；`rtol` 和 `atol` 必须同时给或同时不给。默认还检查数据类型、设备和形状是否一致（`check_dtype=True`、`check_device=True`）。

**常见的坑**：
- **NaN**：默认 NaN 与 NaN 不相等，全是 NaN 的两个结果会失败；需要时传 `equal_nan=True`。但 NaN 通常意味着出错，应先问为什么会有 NaN。
- **默认值随数据类型变**：把输出从 float32 换成 bfloat16，`assert_close` 的容差自动放宽 1 万倍以上（1.3e-6 → 1.6e-2），测试可能悄悄变得很宽松。
- **只比较逐元素**：全部元素都在容差内，不代表整体没问题，例如所有值都系统性偏高 0.5%。
