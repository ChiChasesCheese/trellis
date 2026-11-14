---
id: li-basics-hardware-memory-memory-hierarchy
node: basics.hardware-memory
type: qa
step: 3
---
## Q
计算机的存储层级（寄存器、SRAM、HBM/DRAM、SSD）各有多大、多快？对 AI 推理意味着什么？

## A
离计算单元越近，越快、越小、越贵。以一块 H100 和它所在的服务器为例（数字取量级）：

| 层级 | 是什么 | 容量 | 带宽 |
|---|---|---|---|
| 寄存器 | 计算单元手边的几个格子 | 每 SM 256 KB | 最快 |
| 片上 SRAM | 芯片内部的缓存和共享内存 | 每 SM 256 KB，L2 共 50 MB | 比 HBM 快数倍 |
| HBM 显存 | 封装在芯片旁边的高带宽内存 | 80 GB | 3.35 TB/s |
| 主机内存（DRAM） | CPU 那边的内存条 | 几百 GB 到 2 TB | 经 PCIe 5.0 x16 约 64 GB/s 每方向 |
| NVMe SSD | 磁盘 | 几 TB | 约 7 GB/s |

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 194" font-family="sans-serif" font-size="11">
<text x="170" y="13" text-anchor="middle" fill="currentColor">离计算单元越近：越快、越小、越贵</text>
<rect x="105" y="22" width="130" height="28" rx="3" fill="none" stroke="currentColor"/>
<text x="170" y="40" text-anchor="middle" fill="currentColor">寄存器 · 每 SM 256 KB</text>
<rect x="85" y="56" width="170" height="28" rx="3" fill="none" stroke="currentColor"/>
<text x="170" y="74" text-anchor="middle" fill="currentColor">片上 SRAM · L2 共 50 MB</text>
<rect x="65" y="90" width="210" height="28" rx="3" fill="none" stroke="currentColor"/>
<text x="170" y="108" text-anchor="middle" fill="currentColor">HBM 显存 · 80 GB · 3.35 TB/s</text>
<rect x="35" y="124" width="270" height="28" rx="3" fill="none" stroke="currentColor"/>
<text x="170" y="142" text-anchor="middle" fill="currentColor">主机 DRAM · 至 2 TB · PCIe 约 64 GB/s</text>
<rect x="5" y="158" width="330" height="28" rx="3" fill="none" stroke="currentColor"/>
<text x="170" y="176" text-anchor="middle" fill="currentColor">NVMe SSD · 几 TB · 约 7 GB/s</text>
</svg>

**SRAM 是什么：** 静态随机存储器（static RAM），用晶体管直接做在计算芯片上，速度极快，但占面积大，所以一块 GPU 上只有几十 MB。**HBM/DRAM** 是动态存储器，密度高、容量大，但在芯片外面，要经过接口才能读到。

**对推理的意义：**
- **模型参数放在哪一层决定速度：** 7B 模型 14 GB，GPU 的 SRAM 只有几十 MB，放不下，所以每生成一个 token 都要从 HBM 把参数重读一遍。
- **冷启动：** 从 SSD 加载 14 GB 权重约 2 秒，从网络存储加载可能要几十秒。服务扩容时这段时间不能接流量。
- **不能落到主机内存：** 放不进显存的部分如果每步都要经 PCIe 搬，速度掉 50 倍。
- **一种不同的设计思路：** 如果造一块足够大的芯片，把全部参数都放进片上 SRAM，读参数的带宽就能高出几个数量级。晶圆级芯片走的就是这条路。
