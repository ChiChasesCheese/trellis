---
id: li-accelerators-gpu-gpu-observability
node: accelerators.gpu
type: qa
step: 4
---
## Q
测试推理服务时，怎样判断 GPU 是"真忙"还是"假忙"？`nvidia-smi` 的利用率和 DCGM、Nsight 的指标各说明什么？

## A
**`nvidia-smi` 的 GPU-Util：** 在采样周期内，"至少有一个内核（GPU 上运行的函数）在执行"的时间比例。一个只用了 1 个 SM（GPU 的 132 个"大核"之一）的小内核在跑，也算 100%。所以它只能说明"GPU 不是完全空闲"，不能说明算力或带宽被用满。

**更有用的指标（NVIDIA DCGM 数据中心监控工具提供，可导出到 Prometheus）：**
- **`DCGM_FI_PROF_SM_ACTIVE`：** SM 有线程束在运行的时间比例，在所有 SM 上平均。比 GPU-Util 更能反映"有多少硬件在干活"。
- **`DCGM_FI_PROF_PIPE_TENSOR_ACTIVE`：** Tensor Core（矩阵乘法单元）忙碌的比例。预填充阶段应该较高；小批量生成阶段很低是正常的。
- **`DCGM_FI_PROF_DRAM_ACTIVE`：** 显存接口忙碌的比例，近似"带宽利用率"。小批量生成阶段这个值应该较高，如果很低，说明 GPU 在等别的东西（比如 CPU 调度）。
- **功耗、时钟、温度：** 检查是否降频。

**解读组合：**
- GPU-Util 100%、DRAM 活跃度高、Tensor 活跃度低：生成阶段的正常状态，受带宽限制。
- GPU-Util 100%、DRAM 和 Tensor 都低：大量很小的内核、或者内核之间有空隙，开销在启动和调度上。考虑 CUDA Graph（把一整步的内核录制成一次提交）、算子融合。
- GPU-Util 明显低于 100%：GPU 在等 CPU（分词、调度、Python 开销）或等网络。

**深入分析的工具：**
- **Nsight Systems（`nsys profile`）：** 时间线视图，看 CPU 和 GPU 上每个事件的时间、内核之间的空隙、数据拷贝。回答"时间花在哪里、GPU 有没有在等"。
- **Nsight Compute（`ncu --section SpeedOfLight`）：** 单个内核的分析，报告它达到了峰值算力的百分之几、峰值带宽的百分之几。回答"这个内核本身好不好"。

**测试中的用法：** 性能回归时，除了延迟和吞吐，同时记录 SM 活跃度和 DRAM 活跃度。吞吐下降而 DRAM 活跃度也下降，说明问题在 GPU 之外；DRAM 活跃度不变但吞吐下降，说明读了更多不必要的数据。
