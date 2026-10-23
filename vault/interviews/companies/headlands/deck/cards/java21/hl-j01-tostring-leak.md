---
id: hl-j01-tostring-leak
node: java21.j01-record
type: qa
step: 27
---
## Q
`record` 自动生成的 `toString` 有什么安全隐患？怎么处理？

## A
`toString` 会打印**所有组件**，含密码、令牌、个人信息的组件会被打进日志。

处理：要么**重写 `toString`** 遮掉敏感字段，要么**别把这种东西放进 `record`**。
