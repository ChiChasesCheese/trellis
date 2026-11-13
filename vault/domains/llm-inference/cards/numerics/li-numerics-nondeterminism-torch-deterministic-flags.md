---
id: li-numerics-nondeterminism-torch-deterministic-flags
node: numerics.nondeterminism
type: qa
step: 4
---
## Q
PyTorch 的确定性设置（`torch.use_deterministic_algorithms`、`CUBLAS_WORKSPACE_CONFIG`、随机种子等）能保证什么，不能保证什么？在推理测试里怎么用？

## A
**常用设置：**

```python
import os, random, numpy as np, torch
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"   # 让 cuBLAS 的部分算法可确定
torch.use_deterministic_algorithms(True)            # 遇到没有确定性实现的操作直接报错
torch.backends.cudnn.benchmark = False              # 不按输入形状自动挑选最快的算法
random.seed(0); np.random.seed(0); torch.manual_seed(0)   # 固定所有随机数来源
```

**能保证的：** 同一台机器、同一型号的 GPU、同一软件版本、**同样形状的输入**，重复运行得到逐位相同的结果。
- 使用原子加法（多个线程以不确定的顺序往同一个位置累加）的操作会被替换成确定性实现，没有替代实现的直接报错，让你知道。
- 随机数（dropout、采样）由种子确定。

**不能保证的：**
- **不同的批大小或形状：** 设置只保证"同一种计算重复做结果一样"，不保证"批里 1 个请求和 64 个请求时你的那一行结果一样"。后者叫批不变性，需要专门的内核。
- **不同的 GPU 型号、驱动、库版本：** 不同硬件的内核实现不同。
- **不同的并行配置：** 张量并行的卡数不同，求和的切分和合并顺序就不同。
- **专用推理引擎内部：** vLLM、TensorRT-LLM 使用自己的内核（如注意力内核），这些设置不一定覆盖它们。

**在推理测试里怎么用：**
- **参考实现侧：** 用这些设置让 PyTorch 参考实现完全可复现，这样参考输出可以存成"黄金文件"，每次比较都有一致的基准。
- **定位问题时：** 被测系统在完全相同的条件（同一批组成）下重复运行仍不一致，说明有真正的随机性来源，比如某个内核用了原子操作，或者某处随机种子没被固定。
- **性能代价：** 确定性实现通常更慢，`cudnn.benchmark=False` 也放弃了自动选最快算法，所以只在测试和调试时开启，性能基准要在生产配置下跑。
