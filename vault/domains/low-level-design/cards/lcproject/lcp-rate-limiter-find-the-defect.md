---
id: lcp-rate-limiter-find-the-defect
node: lcproject.lcp-rate-limiter
type: qa
step: 8
tags: [作答]
---
## Q
下面是编程智能体为 LLM 网关限流器写的滑动窗口判定（`limit=1`）。哪里错了？怎么修？哪个测试能抓住它？

```python
def policy_a_limit(self, client_id, endpoint, limit, window_ms):
    now = time.monotonic() * 1000
    q = self._state.setdefault((client_id, endpoint), deque())
    q.append(now)
    while q and now - q[0] > window_ms:
        q.popleft()
    allowed = len(q) <= limit
    remaining = limit - len(q)
    return allowed, remaining, int(q[0] + window_ms - now)
```

## A
**评分点**
- 说出先追加再判断：被拒的请求也留在队列里，重试会把窗口往后推
- 说出被拒时 remaining 为负数：合同要求被拒恒为 0
- 说出边界用 >：恰好满一个窗口的请求仍被计数，应当是 >=
- 说出浮点毫秒相减再截断，可能差 1 ms：应当用整数纳秒
- 说出修法：先清理、再比较，只有放行才追加；被拒直接返回 0
- 说出测试：limit=1、窗口 100，t=0 放行、t=50 被拒、t=100 必须放行，再断言被拒的 remaining == 0

<details class="pt"><summary>参考答案</summary>

四处错：先 `append` 后判断，被拒的请求留痕；被拒时 `remaining` 为负；清理条件 `>` 应为 `>=`；浮点毫秒截断差 1 ms。修法：清理、比较，放行才追加，被拒返回 `remaining=0`，时间用整数纳秒。测试：窗口 100、`limit=1`，t=0 放行、t=50 被拒、t=100 必须放行；并断言被拒的 `remaining == 0`。

</details>

**知识点：** 限流器（Rate Limiter）、AI 的典型错误（Failure Modes）、验证输出（Verification）
