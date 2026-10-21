---
id: nr-amz-s4-starl
node: amazon.outline
type: qa
step: 11
---
## Q
<p class="title">澳洲 Amex 退款费<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- PM 通过正式 help 流程升级：**澳洲商户**看不到 **Amex 退款费**
- 线程在**三个团队**间弹了约 **50 条回复**

<span class="label">T</span>

- 作为**熟悉该领域**的人被路由到我；我 own 的是**答案**，不是工单

<span class="label">A</span>

- **拉数据**而不是看组织架构：六个月按国家数退款费行
- 美国**百万级**，澳洲 **0**，涉及 ~**150** 个商户
- 根因在**配置**：AU 商户的 `fee_refund_policy` 都是 **partial**，逻辑只在 **full** 触发
- 证明**早于迁移**，不是我们引入的回归
- 写结论并附**原始查询**，PM 和另一团队可**自己复跑**
- 第二个无关的费用种类：我说 **"not sure yet"**，给**分层假设**，资深工程师确认

<span class="label">R</span>

- 线程**当天结束**；变成跟踪中的**功能票**

<span class="label">L</span>

- 分歧其实是**知识不对称**时，给所有人**同一份证据**，不争归属

<div class="sources"><b>表达 · business English</b><br>• <b><i>pull the data</i></b> — 拉数据看事实<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I pulled the data by country instead of arguing about whose code it was.”</span><br>• <b><i>reproducible</i></b> — 可复现的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I attached the exact query so the finding was reproducible by anyone.”</span><br>• <b><i>configuration, not code</i></b> — 问题在配置而非代码<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The root cause was configuration, not code: the refund policy was partial.”</span></div>
