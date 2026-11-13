---
id: tr-oracles-float-tolerance-interview
node: oracles.float-tolerance
type: qa
step: 6
---
## Q
面试里被问"你怎么测一个数值计算的结果是对的？容差怎么定？"，怎么答？

## A
- **先说为什么不能用 `==`**：浮点每步都舍入，运算顺序不同结果就不同；并行实现的合并顺序每次可能不同，正确的实现也会差最后几位。
- **说判据公式**：`|actual − expected| ≤ atol + rtol × |expected|`，相对项处理大数，绝对项处理接近 0 的值；工具是 `torch.testing.assert_close` 或 `numpy.testing.assert_allclose`，注意后者默认 `atol=0`、前者默认值随数据类型变化（float32 是 `rtol=1.3e-6, atol=1e-5`，bfloat16 是 `rtol=1.6e-2`）。
- **说参考从哪来**：一个简单可信的参考实现，用 FP64 计算作为"真值"；同时用与被测同精度的参考实现量出合理误差。
- **说容差怎么定**：从数据类型的机器精度和累加长度推算，再用参考误差分布校准，例如定为参考 p99 误差的 2 倍；容差随问题规模变化时写成函数。
- **说防止容差失效**：除逐元素比较外，看整体相对误差和超容差元素比例；定期注入错误检查测试还能抓住缺陷；失败时先查原因，不随手放宽。
- **补单个运算的情况**：数学库函数这类单步运算按 ULP 比较，例如 `assert_array_max_ulp(a, b, maxulp=1)`。
