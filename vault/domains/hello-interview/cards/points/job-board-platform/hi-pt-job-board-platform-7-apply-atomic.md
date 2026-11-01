---
id: hi-pt-job-board-platform-7-apply-atomic
node: qb.lld.job-board-platform.points
type: qa
step: 7
---
## Q
**招聘信息平台 · 投递的原子性**｜出自：招聘信息平台 › 深入 4

招聘平台并发重复点击投递，要保证只产生一条申请，且已关闭或过期的职位不能投。怎么实现 apply？

## A
**要点。** 检查职位开放、检查是否已投、写入是一个复合动作，必须原子：
```python
with self._lock:
    if key in self._applied: return self.apps[self._applied[key]]
```
**数据库版。** 唯一约束 (job_id, seeker_id)，冲突时返回已有记录；职位关闭与投递竞争用 SELECT ... FOR UPDATE 或乐观版本号。
**事件。** 发布放在锁外，避免订阅者阻塞核心流程。
