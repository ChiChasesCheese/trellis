# Resilient Auth with Flaky Third-Party Tokens（应对不可靠第三方鉴权的多区域认证层）

我们的 HTTP/JSON API 平台部署在多个区域，用户和服务的身份鉴权依赖一个外部第三方身份提供方
（第三方 IdP：OAuth/OIDC 登录、或第三方 API key 校验服务）。这个第三方已知不太可靠——间歇性
超时、偶尔整体不可用、校验延迟经常突然飙高，有时候还会返回模糊或过期的结果。我们的平台必须在
第三方降级甚至完全不可用的情况下，继续正确地服务已认证用户的请求，而且**绝不能因为第三方降级
就放松安全校验**（不能因为验证不了就默认放行一个可能已经被吊销的 token）；同时不能因为依赖一
个外部第三方就让平台自己发生全局性中断——某个区域到第三方的网络链路抖动，不该拖垮所有区域。
平台要同时支持多种鉴权方式（基于密钥对的客户端认证、OAuth token 交换），支持 token 刷新、吊销
传播，以及跨区域的时钟偏差容忍。请设计这个系统。

---

**面试环境说明**：Snowflake onsite 或技术电面的 System Design 轮，Hard，45–60 分钟。白板工具未
证实；面试官风格两极，沉默时要自己推进。

**题目原始报告与来源**：
- **LOW（聚合站自建题库，无一手印证）**：PracHub "Resilient Auth with Flaky Third-Party
  Tokens"（Hard，"Multi-region, HTTP/JSON API" 应对不可靠第三方鉴权，171 人做过，2025-09-06）。
  见 `../../../catalog/raw/system_design.md` §1.14 与 §3 第 5 条（该文件明确把这题归为"聚合站
  自建题库，练习价值仅供覆盖面，不代表已证实的 Snowflake 原题"）。**按覆盖面练，不按真题押。**
- 与 Snowflake 的关系：**key-pair authentication**（自包含、运行时零第三方依赖，正是本题该
  推荐的缓解手段）、**Snowflake 对 OAuth 的支持**（本题"依赖第三方 token"场景的原型）、
  **Trust Center**（安全态势看板，可以类比本题里"降级事件/断路器状态"作为安全信号被监控）——
  `../../../01-company-brief.md` §1、§2。**[推断]**
