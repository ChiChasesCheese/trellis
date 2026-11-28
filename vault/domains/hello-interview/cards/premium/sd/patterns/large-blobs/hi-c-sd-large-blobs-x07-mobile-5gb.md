---
id: hi-c-sd-large-blobs-x07-mobile-5gb
node: sd.patterns.large-blobs.exam
type: qa
step: 7
---
## Q
**大文件 · 不稳定网络上传 5GB**｜考点 · 必会

手机上传 5GB 文件，网络时断时续。设计要点？

## A
- **分块：** 分段上传，每块独立预签名 URL；块大小适中，太小请求多，太大重传代价高。
- **续传：** 客户端保存上传会话标识（可放本地存储），重连后 `ListParts` 查已传块，从缺失处继续。
- **进度：** 每块完成即更新进度条。
- **收尾：** 所有块完成后调用完成接口给出块号与校验和，之前文件不可用。

```mermaid
sequenceDiagram
    participant C as 手机
    participant S as 服务器
    participant O as 对象存储
    C->>S: 开始上传
    S-->>C: 会话标识 + 每块预签名 URL
    Note over C: 会话标识存本地
    C->>O: 上传块 1、2、3…
    Note over C,O: 断网，重连
    C->>O: ListParts 查已传块
    O-->>C: 已传块号
    C->>O: 从缺失块继续
    C->>O: 完成接口：块号 + 校验和
    Note over O: 此后文件才可用
```

- **清理：** 生命周期规则 24 到 48 小时清理未完成的分块，避免白付费。
