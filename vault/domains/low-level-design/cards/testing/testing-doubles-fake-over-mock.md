---
id: testing-doubles-fake-over-mock
node: testing.doubles
type: qa
step: 1
---
## Q
测试里该用 mock、stub 还是 fake？为什么常说「优先真实对象和 fake，少用 mock」？

## A
**测结果而不是调用；能用真东西就不替身，替身首选 fake**

- **stub**：返回预设值的替身，只为让被测代码往下走；
- **fake**：一个简化但真能工作的实现（内存里的字典代替数据库）；测试对它读写，行为接近真的；
- **mock**：记录并断言「某个方法被以某个参数调用过」；测的是实现细节；
- **过度 mock 的代价**：重构内部调用（换成批量写）后，行为没变，mock 测试全红；反过来，调用对了但逻辑错，测试也绿；
- **什么时候 mock**：调用本身就是行为（发送邮件、扣款一次且仅一次）。

```python
from unittest.mock import Mock

class FakeStore:                         # 真的能存取，只是在内存里
    def __init__(self): self.d = {}
    def put(self, k, v): self.d[k] = v
    def get(self, k): return self.d.get(k)

def rename(store, old, new):
    store.put(new, store.get(old))

fake = FakeStore(); fake.put("a", 1); rename(fake, "a", "b")
print(fake.get("b"))                     # 1：断言结果

m = Mock(); m.get.return_value = 1; rename(m, "a", "b")
m.put.assert_called_once_with("b", 1)    # 断言调用：换成批量写就坏
```

**知识点：**测试替身（Test Doubles）
