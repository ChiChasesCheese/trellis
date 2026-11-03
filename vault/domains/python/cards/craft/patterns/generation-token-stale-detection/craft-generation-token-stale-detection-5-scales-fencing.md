---
id: craft-generation-token-stale-detection-5-scales-fencing
node: craft.patterns.generation-token-stale-detection
type: qa
step: 5
---
## Q
**代号令牌 · 从熔断器代号到 fencing token**｜模式

客户端 1 拿到锁后长时间垃圾回收停顿，锁过期，客户端 2 拿到锁并写入存储。客户端 1 醒来，仍以为自己持有锁，也去写。怎么让存储拒绝它？

## A
**要点。** 锁服务每次授予租约都附带单调递增的令牌（fencing token）；存储记住见过的最大令牌，拒绝更小的。这就是熔断器代号的分布式版本：旧一轮的写入在落地时被识别并拒绝，而不是依赖旧客户端「自觉知道自己过期」。

```python
class LockService:
    def acquire(self) -> int:
        self.token += 1                  # 每次授予租约，令牌单调递增
        return self.token

class Storage:
    def write(self, token, value) -> bool:
        if self.fencing and token < self.max_token:
            return False                 # 来自旧租约的写入：拒绝
        self.max_token = max(self.max_token, token)
        self.value = value
        return True
```

客户端 1 先拿令牌 1，客户端 2 拿令牌 2 并写入，客户端 1 再写：

```
无 fencing -> 旧写入成功: True 最终值: by client 1 (stale)
有 fencing -> 旧写入成功: False 最终值: by client 2
```

**尺度对照。** 一个进程里的整数代号 → 幂等转账的轮次 → ZooKeeper 事务号、Raft 的任期（term）和乐观锁的版本号：都是让接收方拒绝来自旧领导者或旧版本的写。

**为什么。** 客户端的"我还持有锁"检查在 GC 停顿面前不可靠，检查之后、写入之前它仍可能过期；只有接收方在写入点校验才不留窗口。

**信号。** 租约、领导者选举、分布式锁保护的资源写入；任何「操作者可能在不知情的情况下已经过期」的场景。
