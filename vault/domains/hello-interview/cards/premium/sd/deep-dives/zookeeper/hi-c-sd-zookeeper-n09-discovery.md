---
id: hi-c-sd-zookeeper-n09-discovery
node: sd.deep-dives.zookeeper.notes
type: qa
step: 9
---
## Q
**ZooKeeper · 用途二：服务发现**｜摘要 · 必会

ZooKeeper 怎么做服务发现？现在还常用吗？

## A
- **做法：** 服务启动时在 `/services/<服务名>/` 下创建临时节点，内容是自己的地址；下线或崩溃时节点自动消失，不用显式注销。
- **使用方：** 读取该目录的子节点得到可用实例，选一个连接，并设置监视，实例增减时得到通知。
- **带来的能力：** 动态扩缩、负载均衡、健康检查。
- **现状：** 现在多用专门工具（Consul、etcd）或平台方案（Kubernetes Service、AWS 服务发现），它们实现的模式与 ZooKeeper 很相似，有的内部还用 ZooKeeper。
