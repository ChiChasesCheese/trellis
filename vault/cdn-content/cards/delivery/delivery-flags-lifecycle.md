---
id: delivery-flags-lifecycle
node: delivery.flags
type: qa
---
## Q
A temporary rollout flag has been at 100% for six months. Why is leaving it in place a reliability risk, and what closes the rollout?

## A
Every permanent flag preserves two code paths, expands the test matrix, and leaves a stale emergency control whose semantics may no longer be understood. Assign an owner and expiry when creating it. After stable 100% rollout, remove the losing path and flag reads, verify the simplified path, then retire the control-plane entry with an audit record.

## Q zh
一个 temporary rollout flag 已经保持 100% 六个月。为什么继续保留是 reliability risk，怎样才算结束 rollout？

## A zh
每个永久 flag 都会保留两条 code path、扩大 test matrix，并留下语义可能已无人理解的 stale emergency control。创建时就应指定 owner 和 expiry。在 100% 稳定后，删除 losing path 和 flag read，验证简化后的 path，再带 audit record 地下线 control-plane entry。
