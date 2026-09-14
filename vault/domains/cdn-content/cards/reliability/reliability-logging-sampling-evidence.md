---
id: reliability-logging-sampling-evidence
node: reliability.logging
type: qa
---
## Q
Only 1% of successful requests are logged, and no bad response appears in logs. Can the team conclude the incident is over?

## A
No. Absence in a sampled stream is not evidence of absence. Use unsampled aggregate metrics or black-box probes to establish recovery, preserve all errors and policy violations where affordable, and make the sampling decision observable. Logs explain selected events; they should not be the sole detector or recovery criterion.

## Q zh
只有 1% 的成功 request 被记录，log 中没有出现 bad response。团队能否据此判断 incident 已结束？

## A zh
不能。sampled stream 中没有记录，不代表问题不存在。应使用 unsampled aggregate metric 或 black-box probe 确认恢复；在成本允许时保留全部 error 和 policy violation，并让 sampling decision 可观察。log 用于解释被选中的 event，不应成为唯一 detector 或 recovery criterion。
