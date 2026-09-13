---
id: reliability-incidents-first-mitigation
node: reliability.incidents
type: qa
---
## Q
Immediately after a cache-key rollout, cross-tenant responses appear in one region. What is the first operational sequence?

## A
Declare a security incident, stop the rollout, disable or rollback the new key policy, and bypass or purge affected shared entries according to the safest known path. Preserve request IDs, deployment/config versions, and representative headers before destructive cleanup. Verify recovery with black-box tenant-isolation probes, then assess exposure; root-cause exploration must not delay containment.

## Q zh
cache-key rollout 后，一个 region 立刻出现 cross-tenant response。最先执行的 operational sequence 是什么？

## A zh
声明 security incident，停止 rollout，disable 或 rollback 新 key policy，并按最安全的已知 path bypass 或 purge 受影响的 shared entry。在 destructive cleanup 前保留 request ID、deployment/config version 和 representative header。用 black-box tenant-isolation probe 验证恢复，再评估 exposure；root-cause exploration 不能延迟 containment。
