---
id: bank-linear-ring-buffer
node: bank.structures.linear
type: qa
step: 2
---
## Q
手写容量固定的环形队列，只存 `head` 和 `tail` 两个下标会遇到什么歧义？存 `head` 和 `size` 怎么消除它？`deque(maxlen=n)` 是同一回事吗？

## A
**存 head 和 size，满与空一目了然**

- **歧义**：`head == tail` 既可能是空，也可能是满。常见补救是少用一个槽位（满的条件写成 `(tail + 1) % n == head`），白白浪费一格；
- **`head` 加 `size`**：`size == 0` 是空，`size == capacity` 是满；写入位置是 `(head + size) % n`，没有歧义，也不浪费槽位；
- **环绕靠取余**：下标永远落在 `[0, n)` 内，不会越界；
- **取出后放掉引用**：`buf[head] = None`，否则「已弹出」的对象还被数组引用着，不会被回收；
- **`deque(maxlen=n)` 语义不同**：满了再 `append`，它静默丢掉最旧的元素（覆盖）。下面的 `push` 在满时返回 `False`，拒绝写入。两种合同都合理，题面没写就要先问。

```python
class Ring:
    def __init__(self, cap): self.buf, self.head, self.size = [None] * cap, 0, 0
    def push(self, x):
        if self.size == len(self.buf): return False   # 满了：拒绝，不覆盖
        self.buf[(self.head + self.size) % len(self.buf)] = x
        self.size += 1
        return True
    def pop(self):
        if self.size == 0: raise IndexError("empty")
        x, self.buf[self.head] = self.buf[self.head], None    # 取出并放掉引用
        self.head, self.size = (self.head + 1) % len(self.buf), self.size - 1
        return x

r = Ring(3)
print([r.push(i) for i in range(4)], r.pop(), r.push(9), [r.pop() for _ in range(3)])  # [T, T, T, F] 0 True [1, 2, 9]
```

<details class="pt"><summary>延伸</summary>

要做成「满了覆盖最旧的」，改两处：满时把 `head` 前移一格并让 `size` 不再增加。多线程使用时，`push` 与 `pop` 各自是多步操作，要加锁，或者直接用 `queue.Queue(maxsize=n)`（线程安全，满时阻塞或抛 `queue.Full`）。

</details>

**知识点：**栈、队列、Trie 及变体（Linear & Trie）
