---
id: tr-flaky-causes-numeric-nondeterminism
node: flaky.causes
type: qa
step: 3
---
## Q
数值计算测试在 GPU 或其他加速芯片上偶尔失败：同样的输入，两次运行结果在最后几位不同。原因是什么？怎么让测试稳定？

## A
**原因：浮点加法不满足结合律**。`(a + b) + c` 和 `a + (b + c)` 在浮点下可能不同，因为每一步都会舍入。例如 `(1e16 + 1.0) - 1e16` 得 `0.0`，而 `1e16 - 1e16 + 1.0` 得 `1.0`。在加速芯片上，一次求和被拆给成千上万个并行线程，**谁先加完谁先合并**，合并顺序每次运行都可能不同，结果的最后几位就跟着变。

常见的来源有三种：
- **原子加法（atomic add）**：多个线程同时往同一个位置累加，顺序由硬件调度决定；
- **自动选算法**：库在运行时测试几种实现选最快的，不同运行可能选到不同实现（PyTorch 的 `torch.backends.cudnn.benchmark = True`）；
- **批量大小改变计算拆分**：同一条数据和不同数量的其他数据一起算时，库可能换一种拆分方式，结果略有不同。

**让测试稳定的三种办法**：
- **用容差比较，不用 `==`**：`torch.testing.assert_close(actual, expected)` 默认对 32 位浮点用 `rtol=1.3e-6, atol=1e-5`，按数据类型选默认值；
- **需要逐位可复现时打开确定性模式**：`torch.use_deterministic_algorithms(True)`，在 NVIDIA GPU（CUDA 平台）上还需要设置环境变量 `CUBLAS_WORKSPACE_CONFIG=:4096:8`，并关闭 `cudnn.benchmark`；代价是部分运算变慢，没有确定性实现的操作会直接报错；
- **固定随机种子**：`torch.manual_seed(0)`，只解决随机数，不解决上面的合并顺序问题。

关键区分：结果差在容差内是正常的数值噪声；差得远超容差才是缺陷。
