---
id: hl-bs-s3-followups-b
node: behavioral.stories
type: qa
step: 20
---
## Q
被追问 S3：为什么不把 ACH 加进排除名单？为什么要在迁移里 `DROP`？你补数据了吗？
Why not exclude ACH? Why `DROP` in a migration? Backfill?

## A
- **Why not exclude ACH?** 那会把一个**会响**的检测器变**哑**；手续费确实缺了。
- **Why `DROP` in a migration?** 删掉源文件，**已部署的对象**还在，旧签名仍然可被调用。
- **Backfill?** **向前修复（fix forward）**：错误状态已被下游消费，你需要**纠正记录**，不是回退。我自己**没有**做 backfill。
