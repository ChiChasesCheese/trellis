---
id: craft-exception-family-2-carry-data
node: craft.idioms.exception-family
type: qa
step: 2
---
## Q
**异常家族 · 异常带字段，调用方不解析消息**｜写法

库存不足时，调用方想告诉用户「最多只能买 3 件」。如果异常只有一句消息「A1: 需要 5，可售 3」，调用方要怎么拿到 3？把数据放进异常属性有什么代价？

## A
**要点。** 消息是给人看的，字段是给代码用的。解析字符串很脆弱：改一个措辞、换成英文，所有 `re.search` 都悄悄失效。异常直接带 `sku / requested / available`，调用方读属性就能决策（重试更小的数量、提示缺口），消息只作展示。

```python
class InventoryError(Exception): ...

class OutOfStock(InventoryError):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(f"{sku}: 需要 {requested}，可售 {available}")
        self.sku, self.requested, self.available = sku, requested, available

class OutOfStockP(OutOfStock):
    # pickle 会用 self.args 重建对象；args 只剩一条消息，构造函数要三个参数
    def __reduce__(self):
        return (OutOfStockP, (self.sku, self.requested, self.available))

def reserve(sku: str, qty: int, stock: dict[str, int]) -> None:
    if stock[sku] < qty:
        raise OutOfStock(sku, qty, stock[sku])

try:
    reserve("A1", 5, {"A1": 3})
except OutOfStock as e:
    # 调用方拿字段做决定，不用去解析字符串
    print("建议数量:", e.available, "| 缺口:", e.requested - e.available)

try:
    pickle.loads(pickle.dumps(OutOfStock("A1", 5, 3)))
except TypeError as e:
    print("跨进程传递失败:", e)
e = pickle.loads(pickle.dumps(OutOfStockP("A1", 5, 3)))
print("补了 __reduce__ 后:", e.sku, e.available)
```

实际输出：

```
建议数量: 3 | 缺口: 2
跨进程传递失败: OutOfStock.__init__() missing 2 required positional arguments: 'requested' and 'available'
补了 __reduce__ 后: A1 3
```

**易错。** 异常对象的 `args` 由 `super().__init__(...)` 决定。上面的 `OutOfStock` 把格式化后的消息传给了基类，`args` 只剩一个字符串，而构造函数要三个参数。`pickle` 用 `args` 重建对象，所以跨进程（`multiprocessing`、`concurrent.futures.ProcessPoolExecutor`）传递这个异常，在接收端重建时会抛 `TypeError`。需要跨进程时补一个 `__reduce__`，或者让构造函数的参数都能从 `args` 还原。

**代价。** 字段成了公开接口，改名就是破坏性改动；消息格式不再是契约，字段才是。
