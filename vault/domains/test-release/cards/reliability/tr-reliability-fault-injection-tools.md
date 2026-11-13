---
id: tr-reliability-fault-injection-tools
node: reliability.fault-injection
type: qa
step: 1
---
## Q
在 Linux 测试环境里，进程崩溃、进程卡死、网络延迟丢包、网络分区、磁盘写满这几类故障，分别用什么命令注入？

## A
- **进程崩溃**：`kill -9 <pid>`（SIGKILL，进程无法清理，模拟断电式崩溃）；`kill -15 <pid>`（SIGTERM，模拟正常停机，验证优雅退出）。
- **进程卡死**：`kill -STOP <pid>` 让进程暂停但不退出，端口仍然占着、连接仍然在，模拟长时间垃圾回收停顿或死锁；`kill -CONT <pid>` 恢复。这类"活着但不响应"的故障比崩溃更难被发现，必须测。
- **网络延迟和丢包**：`tc qdisc add dev eth0 root netem delay 200ms 50ms loss 1%`，给网卡加平均 200 ms、抖动 50 ms 的延迟和 1% 丢包；`tc qdisc del dev eth0 root` 移除。
- **网络分区**：`iptables -A INPUT -s <对端IP> -j DROP` 加 `iptables -A OUTPUT -d <对端IP> -j DROP`，切断与某个节点的双向通信；只加一个方向就是非对称分区。测试结束用 `-D` 删除同样的规则。
- **更细粒度的网络故障**：Toxiproxy 在客户端和服务之间做 TCP 代理，可以按连接注入延迟、限速、中途断开，并通过 HTTP 接口在测试代码里开关。
- **磁盘写满**：`fallocate -l 50G /data/fill` 占满分区；或者把数据目录挂在一个很小的 tmpfs 上（`mount -t tmpfs -o size=10m tmpfs /data`）。
- **CPU 和内存压力**：`stress-ng --cpu 8 --vm 2 --vm-bytes 80% --timeout 300s`。
- **Kubernetes 环境**：`kubectl delete pod <name>` 模拟实例被杀；Chaos Mesh 用声明式配置注入 Pod 故障、网络故障、IO 故障。

**每次注入都要配清理**：用 `try/finally` 或 pytest fixture 的 `yield` 保证测试失败时也会删除 `tc` 和 `iptables` 规则，否则会污染后续测试和机器。
