---
id: nr-amz-s3-starl
node: amazon.s3
type: qa
step: 2
---
## Q
【ACH 费用 NULL 传播事故（最难的 bug · fail loudly）】STAR-L 提纲（60–90 秒）

## A
**S**

- 我建的每日**健康检查** "every settled transaction has its Braintree fee" 报警 page 了 on-call

**T**

- 我不是 assignee；把 page **转给自己**，负责**根因、postmortem 和加固**

**A**

- **切片**：缺失的 100% 是新 **standard-ACH** 路径的银行账户交易，~**200 商户**、~**$10M/天**
- **追一笔交易**：sub-kind 是 **NULL**，`'BT_' || NULL` 还是 **NULL**，无类别、无费用、**无报错**
- **根因**：一个函数两个重载，最后的 `MERGE` 调了**没有银行账户分支**的那个
- 有人提议把 ACH 加进检查的排除名单，我**顶回去**，把**数字写下来**
- 队友先落了**止血**；我写 **postmortem** 并做结构性修复
- 结构修复：**单函数**默认参数 + versioned migration **DROP** 旧签名 + 跨 promote 到 fee 的 **e2e** 测试

**R**

- 根因在线程里**几分钟**内给出；**重载设计被整个移除**
- 新 **e2e** 覆盖从 promotion 到 fee 生成

**L**

- 无法映射的 instrument 必须 **fail loudly**，不能什么都不产出
- NULL 传播是 SQL 属性，规则放在**接缝**
