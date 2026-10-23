---
id: hl-os-syscall-cost
node: foundations.os-processes-threads-ipc
type: qa
step: 13
---
## Q
系统调用为什么贵（四点）？实测最轻的系统调用比普通函数调用慢多少，面试说多少最稳妥？

## A
为什么贵：
1. **模式切换**：陷入内核再返回，几十到上百个周期；
2. **安全缓解措施**：2018 年 Meltdown / Spectre 之后，Linux 默认在进出内核时切页表（KPTI）、清分支预测状态；
3. **缓存污染**：内核代码和数据挤掉用户程序的缓存；
4. **本身要做的事**：读文件查页缓存、可能阻塞，网络发送要走协议栈。

实测（macOS，FFM 调 libc）：`write(fd, buf, 1)` 到 `/dev/null` 约 **622 ns**；不进内核的 `abs()` 只要 **4.1 ns**，差约 **150 倍**。Linux 上最轻的系统调用通常 100–几百 ns，受 KPTI 影响很大。面试说「几百纳秒到一微秒」最稳妥。
