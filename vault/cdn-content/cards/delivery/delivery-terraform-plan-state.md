---
id: delivery-terraform-plan-state
node: delivery.terraform-kubernetes
type: qa
---
## Q
Terraform plans to replace a production CDN distribution after an out-of-band console edit. What should happen before `apply`?

## A
Stop and reconcile desired config, refreshed state, and the real resource. Identify whether the console edit was emergency drift or an intentional requirement, import or codify it as appropriate, and review replacement blast radius and lifecycle controls. A plan is a proposed transition, not proof it is safe; never accept destructive replacement merely to make drift disappear.

## Q zh
一次 out-of-band console edit 后，Terraform plan 准备替换 production CDN distribution。在执行 `apply` 前应该做什么？

## A zh
停止并对齐 desired config、refreshed state 与 real resource。判断 console edit 是 emergency drift 还是 intentional requirement，按情况 import 或 codify，并审查 replacement blast radius 和 lifecycle control。plan 只是 proposed transition，不是安全证明；绝不能为了消除 drift 就接受 destructive replacement。
