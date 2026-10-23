---
id: hl-javaq-b-q06-runtime
node: java-questions.b-versions
type: qa
step: 7
---
## Q
Java 8 到 21：偏向锁、容器识别、日志与诊断、线程模型、反射 / 内部 API、NPE 提示信息各有什么变化？

## A
- **偏向锁**：8 默认有（竞争少时快，撤销时要停世界）；15 起默认关闭、后续移除；21 里 `-XX:+UseBiasedLocking` 报 `Unrecognized VM option`。
- **容器**：8 不认 cgroup 限制，容易拿到宿主机核数 / 内存；10 起识别容器限制。
- **日志 / 诊断**：8 是各种 `-XX:+PrintGC*`；现在是统一日志 `-Xlog:gc,safepoint…`；JFR 从 11 起开源（`jcmd JFR.start`）。
- **线程模型**：平台线程 → 21 增加虚拟线程。
- **强封装**：17 起 JDK 内部 API 强封装，反射读 `HashMap.table` 需要 `--add-opens java.base/java.util=ALL-UNNAMED`。
- **NPE 信息**：8 的 `NullPointerException` 没有消息；14 引入有帮助的 NPE 消息，15 默认开启。
