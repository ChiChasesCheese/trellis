---
id: craft-namedtuple-for-keys-1-bare-tuple-keys-swap
node: craft.idioms.namedtuple-for-keys
type: qa
step: 1
---
## Q
**NamedTuple 做键 · 为什么 (调用方, 键) 不该是裸元组**｜写法

幂等转账的键表用 `(调用方, 幂等键)` 这样的元组当字典键，两个元素都是字符串。有人在另一处写成 `(key, client)`，程序照常运行，只是永远查不到。怎样让这种错误更难出现，又不放弃「元组可以当字典键」的好处？

## A
**要点。** 元组按位置解释，不带语义。两个同类型字段顺序写反，类型检查器、运行时都没有任何提示。`NamedTuple` 仍是元组（可哈希，可拆包，可比较，开销和元组一样），但字段有名字：构造时用关键字、读取时用 `k.client`，不再依赖「第 0 位是什么」的记忆。

```python
from typing import NamedTuple

def seen_bare(keys: dict[tuple[str, str], str], client: str, key: str) -> bool:
    return (key, client) in keys                      # 写反了，两个都是 str，毫无提示

keys = {("acme", "pay-123"): "done"}                  # (调用方, 键)
print(seen_bare(keys, "acme", "pay-123"))

class Key(NamedTuple):
    client: str
    key: str

keys2 = {Key("acme", "pay-123"): "done"}
k = Key(key="pay-123", client="acme")                  # 构造时写名字，顺序不再重要
print(k in keys2, k.client, k[0])
print(Key("acme", "pay-123") == ("acme", "pay-123"))   # 仍是 tuple
print(k)
```

实际输出：

```
False
True acme acme
True
Key(client='acme', key='pay-123')
```

**为什么。** 第一行就是静默错误：该命中的查不到，幂等失效，同一个请求被执行第二次。第二行用关键字构造，即使调用处顺序和字段顺序不同也对；`k[0]` 与 `k.client` 同值，所以旧代码用下标访问仍然能工作。

**易错。** 只有用关键字构造才能防住顺序错：`Key("pay-123", "acme")` 位置传参照样写反。要让类型检查器也能发现混用，需要给两个字段不同的类型（用 `NewType` 给两种 ID 各一个类型）。
