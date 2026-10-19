---
id: nr-amz-s8-hook
node: amazon.s8
type: qa
step: 1
---
## Q
【Terraform grant-ownership 7 分钟 RCA（压力下 debug · 主动指出下一个雷）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**A release failed in QA; I was only cc'd, posted the root cause and fix seven minutes later, then scanned the whole repo and flagged the next two failures.**

**适用 LP**

- 主：**Bias for Action**、**Dive Deep**
- 副：Ownership、Insist on the Highest Standards、Earn Trust、Deliver Results

**数字**

- **7 分钟**：从被 cc 到贴出根因 + 修法 + 邻近模块核查
- QA → pre-prod → prod **同天**部署
- 事后全仓库扫描：**79** 个 ownership 资源，**42** 个缺 `outbound_privileges`
- 多数是无害的 `future_*` 变体；`scheme_fees` 模块里 **2 个**与出事的形状完全相同、尚未触发
- 不要说 "the only resource in the whole repo missing it"，不成立。说：「I checked the neighboring modules that day; afterwards I scanned the whole repo and found dozens missing it, mostly harmless future grants, but two real ones in another module that haven't fired yet.」
