---
id: hi-c-sd-zookeeper-n08-config
node: sd.deep-dives.zookeeper.notes
type: qa
step: 8
---
## Q
**ZooKeeper · 用途一：配置管理**｜摘要 · 必会

ZooKeeper 怎么做配置管理？适合放什么配置？

## A
- **做法：** 把数据库连接串、功能开关、服务端点这类配置存在 ZNode 里。
- **真正的价值：** 修改一个 ZNode（如 `enable_reactions` 设为 true），所有监视它的服务器立刻收到通知并更新行为，无需重启；同时具备实时传播、版本管理、原子更新。
- **适合：** 运行时可能变化的动态配置，如定价算法、折扣阈值、维护模式开关。
- **不适合：** 只在发布时才改的静态配置，放文件或环境变量更合适。
- **云上替代：** AWS 有 Systems Manager Parameter Store，Azure 有 App Configuration，在云厂商生态里优先用原生方案。
