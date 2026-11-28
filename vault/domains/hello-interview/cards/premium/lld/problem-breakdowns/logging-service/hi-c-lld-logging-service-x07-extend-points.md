---
id: hi-c-lld-logging-service-x07-extend-points
node: lld.problem-breakdowns.logging-service.exam
type: qa
step: 5
---
## Q
**日志库 · 新需求落在哪个类**｜考点 · 必会

对下面四个新需求，各说明只改哪里：(1) 新增 CSV 输出；(2) 把日志发到网络端点；(3) 每条记录加请求 ID；(4) 同一目的地的阈值改成按级别范围过滤。

## A
- **(1) CSV：** 新增 `Formatter` 实现，其他不改。
- **(2) 网络端点：** 新增 `Sink` 实现（如 `RemoteSink`），`Destination`、`Logger` 不改；要处理超时和失败，也在 sink 内加，或用包装 sink。
- **(3) 请求 ID：** `Record` 加一个字段，`Logger.log` 造记录的那一行多传一个值（通常来自上下文变量）；`Destination`、`Sink` 签名不变，因为它们拿到的是整个记录；只有需要输出该字段的 `Formatter` 要改。这就是把四个参数打包成记录的回报。
- **(4) 范围过滤：** 过滤是 `Destination` 的职责，改它的过滤条件（阈值换成谓词），其他类不动。
- **考察点：** 能把每条改动定位到一个类，说明每个类确实只有一个变化原因。
