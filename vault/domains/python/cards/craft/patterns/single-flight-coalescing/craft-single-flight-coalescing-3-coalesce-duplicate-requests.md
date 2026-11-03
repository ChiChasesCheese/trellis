---
id: craft-single-flight-coalescing-3-coalesce-duplicate-requests
node: craft.patterns.single-flight-coalescing
type: qa
step: 3
---
## Q
**单飞合并 · 同一笔转账被客户端重试了 5 次，怎样只转一次、重试还能拿到结果**｜模式

转账接口带客户端提供的幂等键（idempotency key）。网络超时后客户端会用同一个键重试，且有时重试时第一个请求还没执行完。「查键表，有记录就报错」和「合并」各自的行为是什么？同一个键带着不同金额再来，怎么办？

## A
**要点。** 这是缓存单飞的同一个结构，只是被合并的不是读而是写，而且要保存结果：占键成为拥有者的请求去执行，其余的在 `rec.done` 上等，醒来原样返回第一次的结果。键旁边存「请求指纹」（src、dst、金额、币种）：同键同指纹是重试，同键不同指纹是调用方的 bug，立刻抛 `KeyReuse`。等待有上限，超时抛 `StillRunning`，让客户端稍后再试，而不是再执行一次。

```python
import threading, time
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Req: src: str; dst: str; amount: int                # 请求指纹

@dataclass
class Rec:
    req: Req
    done: threading.Event = field(default_factory=threading.Event)
    result: str | None = None

class KeyReuse(Exception): ...
class StillRunning(Exception): ...

class Transfers:
    def __init__(self, wait=1.0):
        self.keys, self.mu, self.wait, self.executed = {}, threading.Lock(), wait, 0
    def transfer(self, key, req, work_s=0.05):
        with self.mu:                                      # 占键：相当于唯一键插入
            rec = self.keys.get(key); mine = rec is None
            if mine: rec = self.keys[key] = Rec(req)
        if rec.req != req: raise KeyReuse("同一个键不能用于不同的请求")   # 指纹比较
        if mine:                                           # 拥有者：执行，存结果，唤醒等待者
            self.executed += 1; time.sleep(work_s)
            rec.result = f"ok:{req.amount}"; rec.done.set()
            return rec.result
        if not rec.done.wait(self.wait): raise StillRunning()
        return rec.result                                  # 合并：原样返回第一次的结果

t, out = Transfers(), []
ths = [threading.Thread(target=lambda: out.append(t.transfer("k1", Req("a", "b", 100)))) for _ in range(5)]
[x.start() for x in ths]; [x.join() for x in ths]
print("5 次并发重试 ->", set(out), "真正执行次数:", t.executed)
try: t.transfer("k1", Req("a", "b", 999))
except KeyReuse as e: print("同键不同请求:", e)

slow = Transfers(wait=0.01)                                # 拥有者要 0.2 秒，重复请求最多等 0.01 秒
th = threading.Thread(target=lambda: slow.transfer("k", Req("a", "b", 1), work_s=0.2)); th.start()
time.sleep(0.02)
try: slow.transfer("k", Req("a", "b", 1))
except StillRunning: print("第一个请求太慢，重复请求拿到 StillRunning，而不是再执行一次")
th.join()
```

5 个线程用同一个键并发请求：

```
5 次并发重试 -> {'ok:100'} 真正执行次数: 1
同键不同请求: 同一个键不能用于不同的请求
第一个请求太慢，重复请求拿到 StillRunning，而不是再执行一次
```

**为什么。** 只记「做过」不记结果，重试方拿到的是「已处理」，不知道成功还是被拒；记住结果（包括「余额不足被拒」这个结果），重试语义才和第一次完全一致。指纹比较让「同键不同体」失败得很响，不会悄悄返回一个与本次请求无关的结果。

**易错。** 拥有者崩溃（线程挂了、进程重启）时，键永远处于「执行中」，等待者都要超时。需要「接手」机制：记录尝试序号和开始时间，超过期限的拥有者被替换（`attempt += 1`），旧拥有者提交前要检查自己还是不是拥有者，见 generation-token 的叶子。
