---
id: li-accelerators-host-device-rdma-networks
node: accelerators.host-device
type: qa
step: 2
---
## Q
多台机器之间的加速卡怎样高速交换数据？RDMA、InfiniBand、RoCE、GPUDirect RDMA 分别是什么？

## A
**普通网络通信的开销：** 应用数据要经过操作系统内核的网络协议栈，多次在内存中复制，每次收发都要 CPU 参与。数据在 GPU 上时，还要先从显存拷到主机内存，再交给网卡。延迟几十微秒，CPU 开销大。

**RDMA（remote direct memory access，远程直接内存访问）：** 网卡直接读写另一台机器的内存，绕过双方的操作系统内核和 CPU，不做中间拷贝。延迟可以降到几微秒，带宽接近网卡上限。

**两种主流的承载网络：**
- **InfiniBand：** 专为高性能计算设计的网络，原生支持 RDMA，需要专用交换机和网卡。常见速率每端口 400 Gb/s（约 50 GB/s）。
- **RoCE（RDMA over Converged Ethernet）：** 在以太网上跑 RDMA，第二版（RoCE v2）可以跨三层路由。可以用以太网交换机，但对网络配置要求高，需要无损或拥塞控制机制，否则丢包会严重影响性能。

**GPUDirect RDMA：** 网卡直接读写 **GPU 显存**，数据不经过主机内存。多机之间传模型中间结果、KV 缓存时，省掉"显存 → 主机内存 → 网卡"的往返。

**在推理里的用途：**
- **多机模型并行：** 流水线并行在机器之间传激活值，跨机的专家并行做大量的全体对全体交换。
- **预填充与解码分离：** 预填充节点算出的 KV 缓存（每个请求历史 token 每层的键、值向量）传给解码节点。Llama 3.1 70B 的 4,000 token 输入约 1.3 GB，在 400 Gb/s 的链路上约 26 毫秒。
- **加速器之间的直连：** 一些专用加速器也用以太网上的 RDMA 在芯片之间传数据，每跳延迟可低至几微秒。

**验收与排查工具：**
- `ib_write_bw`、`ib_write_lat`（perftest 套件）测 RDMA 带宽和延迟；
- `ibstat`、`ibv_devinfo` 查看端口状态和速率；
- NCCL 的 `NCCL_DEBUG=INFO` 日志会显示实际走的是 InfiniBand、RoCE 还是退化到了普通 TCP（`NET/Socket`），后者性能差一个数量级，是常见的配置错误。
