---
id: api-error-contract-root-exception
node: api.error-contract
type: qa
step: 3
---
## Q
库函数里直接让 `KeyError`、`sqlite3.OperationalError` 穿出公开接口，调用方只好写 `except Exception`。为什么说这是把内部实现写进了接口？公开的错误应该怎么设计？

## A
**公开接口只抛自己的异常层次，底层异常在边界翻译**

- **穿出去的异常就是合同**：调用方一旦写了 `except KeyError`，你就不能把字典换成数据库；
- **一个根异常**：`class ShopError(Exception)`，调用方一句 `except ShopError` 就能接住这个库的全部预期失败；
- **子类各管一种**：`NotFound`、`Conflict`、`InvalidInput`，调用方按类型分支，不看消息；
- **保留因果链**：翻译时写 `raise NotFound(...) from exc`，日志里还能看到原始异常；
- **没预料到的故障不翻译**：磁盘满、连接断开是 bug 或运维问题，原样上抛，别伪装成 `NotFound`。

```python
class ShopError(Exception): ...
class NotFound(ShopError): ...

class Catalog:
    def __init__(self): self._items = {"a1": 10}
    def price(self, sku: str) -> int:
        try:
            return self._items[sku]
        except KeyError as exc:
            raise NotFound(sku) from exc         # 内部的 KeyError 不出门

try: Catalog().price("zz")
except ShopError as e: print(type(e).__name__, "caused by", type(e.__cause__).__name__)
```

**知识点：**接口的错误契约（Error Contract）
