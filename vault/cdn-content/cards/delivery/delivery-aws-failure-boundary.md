---
id: delivery-aws-failure-boundary
node: delivery.aws
type: qa
---
## Q
A content service runs three replicas in one Availability Zone and calls that highly available. What failure boundary is still untested?

## A
All replicas share the same AZ power, network, and capacity boundary. Spread stateless serving capacity across AZs, verify load balancer health and zonal evacuation, and ensure stateful dependencies and quotas do not reintroduce a single-zone dependency. Multi-AZ protects zonal failure; regional failure still needs a separate cross-region strategy.

## Q zh
content service 在一个 Availability Zone 内运行三个 replica，并称其 highly available。哪个 failure boundary 仍未被测试？

## A zh
所有 replica 共享同一个 AZ power、network 和 capacity boundary。应把 stateless serving capacity 分布到多个 AZ，验证 load balancer health 与 zonal evacuation，并确保 stateful dependency 和 quota 没有重新引入 single-zone dependency。multi-AZ 只保护 zonal failure；regional failure 仍需要独立 cross-region strategy。
