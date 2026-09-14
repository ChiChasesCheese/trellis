---
id: trust-center-continuous-drift
node: security.trust-center-posture
type: qa
tags: [grown]
---
## Q
上线前已经人工做过一次完整的安全配置检查，为什么还需要信任中心（Trust Center）定期扫描？

## A
安全配置会漂移（configuration drift）：新建用户忘了开 MFA、临时放开的网络策略没有收回、为排障授予的 ACCOUNTADMIN 没有撤销。一次性检查只反映当时的快照，定期扫描才能在漂移发生后尽快发现。扫描按计划运行也意味着扫描本身会消耗计算资源（产生少量费用），扫描频率需要在发现时效与成本之间权衡。
