---
id: concurrency-depth-lock-scope-remote-call
node: concurrency-depth.compound-actions
type: qa
step: 3
---
## Q
`charge` 要先看余额、再调一个 50 ms 的远程风控、最后扣款。锁该罩多大？远程调用放锁里和放锁外各有什么后果？

## A
**锁罩状态，不罩慢调用：先预留，锁外调用，再结算**

- **远程调用在锁里**：8 个线程各调一次，全部排队，耗时约为锁外的 7 倍（各 sleep 50 ms 实测），而且远程挂住就把整个服务卡住；
- **只在锁外检查**：先 `if bal < n` 再调远程、再扣款，两次检查之间别人也过了检查。余额 100、8 个线程各扣 100，实测 50/50 轮出现负余额；
- **预留（reserve）**：锁内检查 `bal - held >= n` 并登记 `held += n`，让别的线程看到这笔钱已被占用；
- **结算（settle）**：远程返回后重新进锁，释放预留，成功才扣款；失败或抛异常也要释放预留，所以结算放在 `finally` 里；
- **不变量**：任何时刻 `bal - held >= 0`，由锁保证。

```python
import threading
class Wallet:
    def __init__(self, bal):  self.bal, self.held, self._l = bal, 0, threading.Lock()
    def charge(self, n, remote):
        with self._l:                          # 1 预留
            if self.bal - self.held < n: return False
            self.held += n
        ok = False
        try:
            ok = remote(n)                     # 2 慢调用在锁外
        finally:
            with self._l:                      # 3 结算
                self.held -= n
                self.bal -= n * ok             # 成功才扣（True 当 1）
        return ok
```

<details class="pt"><summary>延伸</summary>

这是乐观并发的一种：另一种是不预留，结算时检查版本号，变了就重试。冲突少时更省，冲突多时重试会互相打架。

</details>

**知识点：**复合操作（Compound Actions）
