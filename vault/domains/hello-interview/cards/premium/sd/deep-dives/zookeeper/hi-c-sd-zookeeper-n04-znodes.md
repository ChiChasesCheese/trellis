---
id: hi-c-sd-zookeeper-n04-znodes
node: sd.deep-dives.zookeeper.notes
type: qa
step: 4
---
## Q
**ZooKeeper · ZNode：小数据、多节点的树**｜摘要 · 必会

ZooKeeper 的数据怎么组织？适合存什么，不适合存什么？

## A
- **层次树：** 像文件系统的目录树，每个节点叫 ZNode，用路径标识，如 `/app1/config`。
- **和目录不同：** ZNode 本身可以存数据，也有元数据（版本等）。
- **存小不存大：** ZNode 用来存协调数据，数据通常很小（不到 1 MB），ZNode 的数量可以很多（数千个量级）。图片、长文档不属于这里。
- **聊天应用的树：** `/chat-app/servers/server1` 存服务器地址；`/chat-app/users/alice` 存 "server1"；`/chat-app/config/max_users` 存最大用户数。查 Bob 在哪台机器就读 `/chat-app/users/bob`。
- **规模提示：** 真实应用有上百万在线用户，不应每个用户一个 ZNode；改用一致性哈希，ZooKeeper 只登记服务器，用户由哈希算出去哪台。
