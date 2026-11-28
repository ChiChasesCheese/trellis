---
id: hi-c-sd-cassandra-n13-hinted-handoff
node: sd.deep-dives.cassandra.notes
type: qa
step: 13
---
## Q
**Cassandra · Hinted Handoff：节点离线时的写入**｜摘要 · 必会

目标副本暂时下线时，写请求怎么继续？它能不能代替修复？

## A
- **机制：** 协调者发现目标副本被判定下线，就把这次写入暂存在本地，称为提示（hint）；写入对其余副本照常进行。
- **补发：** 等该节点被检测到恢复在线后，持有 hint 的节点把数据重放给它，让它补上错过的写入。
- **只管短期：** hint 的寿命短，适合短暂离线。节点离线很久时，hint 已失效或不完整，需要通过读修复（read repair）或整体重建来追平。
- **意义：** 让短暂故障对写入透明，且不要求手工干预。
