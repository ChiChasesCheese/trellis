# 速记卡 · 安全领域词汇（20 张；面试里自然说出口即可，不背定义）

> 依据：Abnormal 产品页与 JD（`catalog/raw/official.md` O-1、O-4、O-5）+ 行业通用术语。英文是面试里用的说法。

1. **BEC (Business Email Compromise)**：冒充高管/供应商骗转账或礼品卡；无恶意链接/附件，靠**行为异常**（新发件人、display name 冒充、reply-to 不同）识别。Abnormal 起家的问题。
2. **VEC (Vendor Email Compromise)**：供应商真实邮箱被盗后发假发票——发件人"可信"，所以 allowlist 不能压过内容/行为信号。
3. **ATO (Account Takeover)**：账号被盗用；信号：impossible travel、新设备/国家、MFA 疲劳、邮箱规则被改（自动转发到外部）。
4. **Impossible travel**：两次登录的距离 / 时间差 > 物理可能速度（如 > 900 km/h）。误报源：VPN、移动网络出口、IP 地理库误差。
5. **Insider risk / insider threat**：内部人（或伪装成员工的外部人）造成的风险：数据外泄、破坏、欺诈。
6. **Infiltration**：对手以求职者身份进入企业（合成身份、代面、VPN、VoIP、"笔记本农场"）——Chi 团队的产品方向。
7. **Synthetic identity / persona**：拼凑或 AI 生成的身份（照片、简历、LinkedIn）。
8. **VoIP number**：虚拟号码（Google Voice 等），本身合法常见 → **弱信号**，需与其它信号组合。
9. **IP geolocation mismatch**：申请填写的国家 vs 提交/登录 IP 的国家不一致；VPN/hosting ASN 是放大器。
10. **ASN**：自治系统号，标识 IP 段所属网络（云厂商、VPN 提供商、ISP）。"hosting ASN" 常意味着 VPN/代理。
11. **IOC (Indicator of Compromise)**：已知恶意的 IP、域名、哈希、号码等；"match against known indicators"。
12. **TTPs (Tactics, Techniques, and Procedures)**：对手的行为模式（MITRE ATT&CK 词汇）；JD nice-to-have 原词。
13. **Correlation / link analysis**：跨记录找共享属性（电话前缀、IP /24、简历指纹）→ 聚类成 campaign；注意常见共享值（公司 NAT、大学网段、招聘代理）。
14. **Evidence timeline**：每个结论附来源与时间的证据链，给人工审核；产品原话 "each signal cited with its source"。
15. **Disposition**：审核结论（cleared / escalated / confirmed malicious）——是 ground truth 与反馈回路的来源。
16. **Allowlist / suppression**：抑制已知良性；**必须带范围（租户、规则、条件）、留痕、可过期**，且不能压过强信号。
17. **Baseline / UEBA**：按用户/实体的正常行为基线（User and Entity Behavior Analytics）；冷启动用同组（部门/角色）基线。
18. **SOC / SOAR**：安全运营中心 / 编排自动化平台；webhook 通知、工单、自动处置的消费者。
19. **DLP / exfiltration**：数据防泄漏 / 外泄：大量下载、外部分享、转发到个人邮箱，离职前窗口风险最高。
20. **Precision vs alert fatigue**：误报率 × 事件量 = 每天告警数；"99.5% threshold on hundreds of millions of rows is still millions of alerts a day"（[[S6]]）。
