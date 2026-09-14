---
id: reliability-correlated-failures
node: reliability.availability
type: qa
---
## Q
Two replicas at 99.9% "should" give six nines in parallel. Why do real systems get far less, and what restores some of the promised benefit?

## A
The parallel formula assumes **independent** failures; real faults are correlated:

- **Shared fate**: same rack/AZ/power, same load balancer, same cloud control plane.
- **Same software**: one bad deploy or config push takes out every replica simultaneously — the most common correlated fault.
- **Load coupling**: one replica's death shifts traffic and overloads the survivors (cascade).

Restore independence by spreading across **failure domains** (AZs/regions), staggering rollouts so versions never change everywhere at once, and removing shared hard dependencies from the redundant path. See [[reliability-serial-parallel-composition]].

## Q zh
在 99.9% 的两个副本"应该"给出六个九的并联中。为什么真实系统获得远少得多，什么恢复了一些承诺的好处？

## A zh
并联公式假设**独立**故障；真实故障是相关的：

- **共享命运**：同机架/AZ/电力、同负载均衡器、同云控制平面。
- **相同软件**：一个坏部署或 config 推送同时击倒每个副本——最常见的相关故障。
- **负载耦合**：一个副本的死亡转移流量并使幸存者过载（级联）。

通过跨**故障域**（AZ/区域）传播、错开推出以便版本永不同时改变所有地方、移除冗余路径中的共享硬依赖来恢复独立性。见 [[reliability-serial-parallel-composition]]。
