---
id: msd-training-experiments-determinism
node: training.experiments
type: qa
step: 2
---
## Q
同一份代码、同一份数据训练两次，结果为什么会不同？在 PyTorch 里怎样尽量做到逐位一致，代价是什么？

## A
**随机性从哪里来：**
- **初始化**：参数的初始值是随机数。
- **数据顺序**：每轮训练打乱数据的顺序，以及数据增强（随机裁剪等）。
- **Dropout**：训练时随机屏蔽一部分中间结果。
- **GPU 的非确定性运算**：很多 GPU 算子用原子加法并行累加，加法顺序每次不同。浮点加法不满足结合律，(a + b) + c 和 a + (b + c) 在最后几位可能不同，误差再经过成千上万步训练被放大。
- **算法自动选择**：cuDNN 会对卷积试跑几种实现选最快的，每次选中的可能不同。
- **多进程数据加载**：每个加载进程有自己的随机状态。

**尽量逐位一致的设置：**
```python
import os, random, numpy as np, torch
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"   # 让 cuBLAS 可确定
random.seed(0); np.random.seed(0); torch.manual_seed(0)  # 后者也设好所有 GPU
torch.use_deterministic_algorithms(True)  # 遇到不确定的算子直接报错
torch.backends.cudnn.benchmark = False     # 不自动挑算法
g = torch.Generator().manual_seed(0)
loader = DataLoader(ds, shuffle=True, generator=g,
                    num_workers=4, worker_init_fn=seed_worker)
```
`seed_worker` 在每个加载进程里用 `torch.initial_seed()` 派生种子并设好 NumPy 和 random。

**代价与边界：**
- 确定性算法通常更慢，有的慢 10%–30%，有的算子没有确定性实现，只能报错或换写法。
- 即使全部设置好，**换 GPU 型号、换 CUDA 或 PyTorch 版本、换卡数**仍可能得到不同结果，因为底层实现和累加顺序变了。
- 所以逐位一致只在"同硬件、同软件、同卡数"内成立；跨环境只能要求**统计上一致**：指标落在多种子运行的波动范围内。
