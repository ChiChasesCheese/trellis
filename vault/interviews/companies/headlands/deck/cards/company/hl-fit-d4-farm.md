---
id: hl-fit-d4-farm
node: company.fit
type: qa
step: 16
---
## Q
JD 日常工作 "Investigate new technologies to improve stability, scalability, and performance of a distributed computing farm"，你的相邻经验和要避免的说法是什么？

## A
评级：**部分**。

- 实习：Kafka Connect 在 K8s，一个 topic 一个 Deployment，并行度 = replicas × tasks.max，上限 = partition 数；Airflow DAG 调度 Spark 作业；Quant-Stroller 在 8-GPU 服务器上跑 PyTorch + 自托管 CI。
- 边界：我是消费 / 落库 / 校验侧，**没有运维过集群**，别说"运维过集群"。
- 说法：学到的是"并行度被最窄的分区资源封顶"。
- 要补：K8s 基础、计算集群调度。
