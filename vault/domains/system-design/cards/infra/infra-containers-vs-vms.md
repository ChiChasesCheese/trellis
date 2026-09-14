---
id: infra-containers-vs-vms
node: infra.containers
type: qa
---
## Q
Containers and VMs both isolate workloads. What is the actual isolation mechanism of each, and what does the difference buy in density and cost in security?

## A
- **VM**: a hypervisor virtualizes hardware; every guest boots its **own kernel**. Strong boundary, but seconds to boot and GBs of overhead per instance.
- **Container**: ordinary processes on a **shared host kernel**, isolated by **namespaces** (what they can see — PIDs, network, mounts) and **cgroups** (what they can use — CPU, memory). Millisecond starts, MBs of overhead → order-of-magnitude better packing density.
- The shared kernel is the security catch: one kernel exploit escapes the container. That's why multi-tenant platforms run untrusted code in **microVMs** (Firecracker, gVisor) — VM-grade boundary at near-container startup cost.

## Q zh
容器和 VM 都隔离工作负载。各的实际隔离机制是什么，在密度中的差异以及在安全中的代价是什么？

## A zh
- **VM**：hypervisor 虚拟化硬件；每个客机启动它自己的**内核**。强边界，但启动需要秒和每个实例 GB 开销。
- **容器**：**共享主机内核**上的普通进程，由 **namespace**（它们能看什么——PID、网络、挂载）和 **cgroup**（它们能用什么——CPU、内存）隔离。毫秒启动，MB 开销→一个数量级更好的打包密度。
- 共享内核是安全抓住：一个内核漏洞逃逸容器。这就是为什么多租户平台在 **microVM**（Firecracker、gVisor）中运行不可信代码——VM 级别边界以接近容器启动成本。
