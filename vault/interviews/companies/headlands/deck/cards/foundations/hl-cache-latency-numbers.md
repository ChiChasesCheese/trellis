---
id: hl-cache-latency-numbers
node: foundations.cpu-cache-locality
type: qa
step: 4
---
## Q
经典的延迟数字表里，这些操作各约多少：普通指令、L1 读、分支预测失败、L2 读、互斥锁加解锁、主内存读、顺序读 1 MB 内存、磁盘寻道、美欧往返？

## A
- 普通指令：1 ns；L1 读：0.5 ns；
- 分支预测失败（branch misprediction）：5 ns；
- L2 读：7 ns；互斥锁（mutex）加解锁：25 ns；
- 主内存读：100 ns；
- 经 1 Gbps 网络发 2 KB：20,000 ns；
- 顺序读 1 MB 内存：250,000 ns；
- 磁盘新位置寻道：8 ms；顺序读 1 MB 磁盘：20 ms；
- 美国与欧洲往返：150 ms。

这些数字来自约 2000 年代的硬件，**记量级和比例，不是精确值**。
