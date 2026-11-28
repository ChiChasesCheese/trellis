---
id: hi-c-sd-temporal-b01-versioning
node: sd.deep-dives.temporal.beyond
type: qa
step: 1
---
## Q
**Temporal · 部署新版本 Workflow 代码会怎样：版本管理与非确定性错误**｜拓展 · 加分

有 10 万个运行了 3 天的订单 Workflow，你改了 Workflow 代码，在 `requestShipment` 前新增了一个 Activity，然后部署。会发生什么？

## A
- **问题：** 在途 Workflow 用新代码重放时，历史里记录的第 3 个事件是 `requestShipment`，新代码在这个位置却想调用新增的 Activity，对不上，产生非确定性错误，Workflow 卡住。
- **做法一，补丁（patching）：** 用版本分支标记 `if patched("add-fraud-check")`，老的历史走旧路径，新启动的 Workflow 走新路径；等所有老 Workflow 结束后再清除旧分支。
- **做法二，按 worker 版本路由：** 老 Workflow 继续由旧版本的 worker 运行，新 Workflow 由新版本运行（Worker Versioning）。
- **做法三，重放测试：** 在 CI 里用生产环境导出的真实历史对新代码做重放，发现不兼容再合并。
- **含义：** 重放模型的代价是：长时间运行的流程修改代码要十分小心，这是工作流引擎的运维要点。
