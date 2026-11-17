---
id: data-invariants-leak-rep
node: data.invariants
type: qa
step: 5
---
## Q
`LoanStore.get(id)` 直接返回内部保存的 dict，为什么这让不变量名存实亡？封装到底在保护什么？

## A
**封装保护的是“只有方法能改内部状态”**

- 不变量靠“所有写入都经过带校验的方法”才成立；
- **泄漏**：调用方拿到内部 dict，`loan["status"] = "active"` 就绕过了放款检查、审计和计数；
- **同类的漏洞**：返回内部 list、保存调用方传入的 list、可变默认参数；
- **补法**：返回副本、冻结的 dataclass、只读视图（`types.MappingProxyType`），或只返回需要的值；拷贝与只读视图的取舍在防御性拷贝一叶。

```python
from types import MappingProxyType

class Loans:
    def __init__(self): self._rows = {1: {"status": "pending", "owed": 100}}
    def get_leaky(self, i): return self._rows[i]
    def get_view(self, i): return MappingProxyType(self._rows[i])

store = Loans()
store.get_leaky(1)["status"] = "active"      # 没经过放款，不变量被绕过
print(store.get_leaky(1)["status"])
try: store.get_view(1)["owed"] = -5
except TypeError as e: print("blocked:", e)
```

<details class="pt"><summary>延伸</summary>

`MappingProxyType` 只包一层：里面的值本身可变（嵌套 list）时，调用方仍能改。要让整个结构不可变，得把嵌套的值也换成不可变类型，比如元组、`frozenset`。

</details>

**知识点：**不变量与封装（Invariants）
