---
id: nr-amz-s8-starl
node: amazon.s8
type: qa
step: 2
---
## Q
【S8 · Terraform grant-ownership 7 分钟 RCA（压力下 debug · 主动指出下一个雷）】STAR-L 提纲（60–90 秒）

## A
**S**

- **Snowflake 基础设施**仓库的发布在 **QA** 失败：`GRANT OWNERSHIP` 被拒
- 一个 reviewer 角色已持有依赖的 **USAGE** 授权

**T**

- 别人被**分配**去查，我只是 **cc**；但发布被卡住

**A**

- **读错误**，对上我熟悉的授权结构
- **7 分钟**贴出根因：ownership 资源没设 `outbound_privileges`
- 贴**一行修法** `outbound_privileges = "REVOKE"` + **邻近模块**核查
- **问了**能否直接推；PR 合入
- **事后**扫**全仓库**找同样的遗漏
- 标出另一模块里 **2 个**同形、还没触发的资源

**R**

- QA、pre-prod、prod **同一下午**部署
- 扫描：几十个缺该参数，多数是无害 `future_*`；挖出 **2 个真实风险**，我不说它们已修

**L**

- **修这一个**和**消灭这一类**是两件事
- 宁可负责「这是下一个」
