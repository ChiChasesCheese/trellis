---
id: hi-c-lld-amazon-locker-n06-token-compartment
node: lld.problem-breakdowns.amazon-locker.notes
type: qa
step: 6
---
## Q
**快递柜 · `AccessToken` 与 `Compartment` 的接口**｜摘要 · 必会

取件码和格口各自暴露哪些方法？整套类设计遵循什么原则？

## A
- **`AccessToken`：** 状态是码、过期时刻、对应格口；方法是 `is_expired`、取格口、取码。它拥有过期时刻，所以过期判断归它；它只回答"过期了吗"，由调用者决定怎么处理。
- **`Compartment`：** 状态是尺寸和 `occupied`；方法是读尺寸、读占用、`mark_occupied`、`mark_free`、`open`。只管物理状态，没有业务逻辑。
- **`Size`：** 小、中、大的枚举。
- **原则：信息专家（Information Expert）：** 谁拥有数据，谁负责处理。`Locker` 做分配和映射，`AccessToken` 管过期，`Compartment` 管自己的物理状态。
- **返回值设计：** 存件只返回码，因为门会自动打开；取件返回空，因为门打开就是反馈。
