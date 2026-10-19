---
id: nr-amz-s3-starl
node: amazon.outline
type: qa
step: 8
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- 我建的每日**健康检查** "every settled transaction has its Braintree fee" 报警 page 了 on-call

<span class="label">T</span>

- 我不是 assignee；把 page **转给自己**，负责**根因、postmortem 和加固**

<span class="label">A</span>

- **切片**：缺失的 100% 是新 **standard-ACH** 路径的银行账户交易，~**200 商户**、~**$10M/天**
- **追一笔交易**：sub-kind 是 **NULL**，`'BT_' || NULL` 还是 **NULL**，无类别、无费用、**无报错**
- **根因**：一个函数两个重载，最后的 `MERGE` 调了**没有银行账户分支**的那个
- 有人提议把 ACH 加进检查的排除名单，我**顶回去**，把**数字写下来**
- 队友先落了**止血**；我写 **postmortem** 并做结构性修复
- 结构修复：**单函数**默认参数 + versioned migration **DROP** 旧签名 + 跨 promote 到 fee 的 **e2e** 测试

<span class="label">R</span>

- 根因在线程里**几分钟**内给出；**重载设计被整个移除**
- 新 **e2e** 覆盖从 promotion 到 fee 生成

<span class="label">L</span>

- 无法映射的 instrument 必须 **fail loudly**，不能什么都不产出
- NULL 传播是 SQL 属性，规则放在**接缝**

<div class="sources"><b>表达 · business English</b><br>• <b><i>scope the problem</i></b> — 先把问题范围划清楚<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I scoped the problem by slicing the missing fees by payment type and source.”</span><br>• <b><i>walk it back</i></b> — 沿链路往回追<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I walked it back through the promote procedure until I found the overwriting MERGE.”</span><br>• <b><i>structural fix</i></b> — 结构性修复<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“After the stopgap I made a structural fix: one function, and the old signature dropped.”</span></div>
