---
id: li-accelerators-host-device-host-device-path
node: accelerators.host-device
type: qa
step: 1
---
## Q
数据从主机（CPU 和内存）到加速卡要经过什么通路？PCIe 带宽是多少？什么是 DMA 和锁页内存（pinned memory），它们为什么重要？

## A
**通路：** 主机内存 → PCIe 总线 → 加速卡的显存（HBM）。PCIe 是服务器上连接 CPU 和外设（GPU、网卡、NVMe 硬盘）的标准高速总线。

**PCIe 带宽（x16 插槽，每个方向）：**
- PCIe 4.0：约 32 GB/s
- PCIe 5.0：约 64 GB/s
- 对比 H100 显存带宽 3.35 TB/s，PCIe 慢约 50 倍。所以模型参数必须提前放进显存，不能每一步从主机搬。

**DMA（direct memory access，直接内存访问）：** 由专门的硬件引擎在主机内存和设备内存之间搬数据，不需要 CPU 逐字节参与。CPU 只负责发出"把这块搬过去"的命令，然后可以去做别的事，搬运和计算可以同时进行。

**锁页内存（pinned / page-locked memory）：** 操作系统保证不会被换出到磁盘、物理地址不会变的内存。
- DMA 引擎需要稳定的物理地址。普通（可分页）内存在拷贝前要先复制到一块临时的锁页缓冲区，多一次拷贝，而且无法异步进行。
- 用锁页内存，拷贝更快，并且可以和 GPU 计算重叠。

```python
x = torch.randn(1024, 4096).pin_memory()      # 分配锁页内存
y = x.to("cuda", non_blocking=True)            # 异步拷贝，CPU 立即返回
```

**推理里哪些地方走这条路：**
- **加载模型：** 7B 模型 14 GB，按 PCIe 5.0 理论值约 0.2 秒；实际瓶颈通常是从磁盘或网络存储读文件。
- **每一步的输入和输出：** token 编号、位置编号送进去，新 token 取回来。数据很小，但每步都有，延迟（每次几微秒到几十微秒）会累积。
- **KV 缓存卸载：** 把暂时不用的 KV 缓存（每个请求历史 token 的中间结果）挪到主机内存，用时再搬回。几 GB 的数据要搬几十到上百毫秒。

**测试检查点：** 用 `nvidia-smi -q` 查看 PCIe 链路的当前代数和宽度（Link Gen、Link Width），确认没有降到 x8 或低一代；用 CUDA 示例程序 `bandwidthTest` 或 `nvbandwidth` 实测主机与设备之间的带宽，作为机器验收项。
