---
id: errors-boundary-validate-before-mutate
node: errors.boundary-validation
type: qa
step: 5
---
## Q
服务的 `add_comment(body)` 既要校验 `body`，又要拿锁、分配 ID、写入。校验放在哪一步？放错了会怎样？

## A
**校验在拿锁和改状态之前**

- **顺序**：校验 → 拿锁 → 查存在性 → 分配 ID → 写入；
- **失败不留痕**：非法输入在改状态前抛出，ID 计数器、列表、审计行都没动，下一次成功拿到的 ID 仍是连续的；
- **锁更短**：校验不碰共享数据，放在锁外，并发时少一个排队点；
- **反例**：先 `next_id += 1` 再校验，失败的请求烧掉一个 ID，“第一条成功评论的 id 是 1”的测试就变成 2。

```python
import threading

class Comments:
    def __init__(self):
        self._lock, self._next_id, self._items = threading.Lock(), 1, []
    def add(self, body):
        if not isinstance(body, str) or not body.strip():
            raise ValueError("body")           # 状态还没碰
        with self._lock:
            cid, self._next_id = self._next_id, self._next_id + 1
            self._items.append((cid, body))    # strip 只用来判空，存的是原值
            return cid
# add("   ") 抛 ValueError；之后第一次成功的 add(" hi ") 仍返回 1
```

**知识点：**边界校验（Validate at the Boundary）
