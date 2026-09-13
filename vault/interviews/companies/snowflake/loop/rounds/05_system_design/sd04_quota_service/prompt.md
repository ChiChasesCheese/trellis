# Quota Service（多租户配额，多个上游服务共用）

我们内部有好几个业务系统都需要对用户/租户做资源配额限制——比如某个存储上传服务要限制"每个租户每天最多上传多少 GB"，某个计算服务要限制"每个租户同时能占用多少并发资源"。现在这些限制都是各团队自己在各自服务里攒的一段计数逻辑，重复建设而且口径不一致，我们想抽出一个统一的 Quota Service，让所有这些上游业务系统都调用它来做"我这次操作允许不允许"的判断和扣减。这里有一个核心矛盾：一方面，配额这种东西必须是**强一致**的——如果一个用户的配额是 100，我们绝对不能让并发的多个请求同时通过检查、最后实际消耗掉了 120（这是要花钱赔付或者被滥用的真实业务风险）；但另一方面，这个服务会被非常高频地调用（每一次业务操作前都要问一下配额），如果每次调用都要走一次强一致的中心化服务，延迟和这个中心服务本身的吞吐压力都会成为问题。而且我们是多个区域部署的，同一个租户的操作可能来自不同地理区域，配额需要在全局层面被正确地统计，不能出现"各区域各算各的、加起来超发"的情况。请设计这个 Quota Service。

---

**面试环境说明**：这是 Snowflake 技术电面或 onsite 的 System Design 轮，时长 45–60 分钟。白板工具未证实；面试官风格两极分化。这道题的核心矛盾（强一致 vs 高频调用 vs 多区域）是评分的主线，候选人需要清楚地说出这是一个"正确性 vs 延迟"的权衡问题，而不是简单套用某个缓存方案。

**题目原始报告与来源**（置信度见 `catalog/raw/system_design.md` §1.2）：
- **一手**："Design a Quota System used by multiple upstream services" —— 1p3a thread-1137616 搜索摘要（**中**，复用 `../../raw/process_research.md` §3.2 #8）。
- **聚合站细节版**（与一手同源，细节更完整）：Quota Service 要求 **strong consistency** 防止 client 超过资源上限，应用场景举例为"文件上传"；API 需要支持 `SET quota` —— staffengprep.com（**中**）。
- **另一变体**："Design a Multi-Tenant Quota System" / "Global Multi-Tenant Quota Service (Single Global Quota per User)"，Hard 难度 —— PracHub（**低**）。
- 归类页面显示该题族标签为 "Quotas/Distributed-Systems/Rate-Limiting/Caching"（60 min 独立报告）—— staffengprep.com（**中**）。
- 整体置信度 **MED**。追问汇总（原文已给出）：强一致 vs 最终一致的取舍（配额超发的业务后果 vs 延迟）；本地缓存配额 + 定期同步 vs 每次请求打中心服务；多区域部署下的全局配额如何不产生单点瓶颈；client 侧限流与服务端配额的分层。
