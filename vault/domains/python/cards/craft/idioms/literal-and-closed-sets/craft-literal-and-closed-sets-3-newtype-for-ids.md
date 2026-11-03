---
id: craft-literal-and-closed-sets-3-newtype-for-ids
node: craft.idioms.literal-and-closed-sets
type: qa
step: 3
---
## Q
**封闭取值集 · 账户 ID 和调用方 ID 都是 str，怎么防止传错**｜写法

转账函数有三个字符串参数：源账户、目标账户、调用方。有人调用时把调用方放在了账户的位置，类型都是 `str`，程序照常运行，只是转错了账。`NewType` 能防住什么，防不住什么？

## A
**要点。** `NewType("AccountId", str)` 在类型检查器眼里是一个独立类型，`ClientId` 又是另一个；互相传错会被报错。运行时它没有任何成本：`AccountId("acc-1")` 就是原来的字符串，不新建对象，也不做校验。所以它防的是「混用」，不是「非法值」。

```python
from typing import NewType

AccountId = NewType("AccountId", str)
ClientId = NewType("ClientId", str)

def transfer(src: AccountId, dst: AccountId, client: ClientId) -> str:
    return f"{client}: {src}->{dst}"

a, b, c = AccountId("acc-1"), AccountId("acc-2"), ClientId("acme")
print(transfer(a, b, c))
print(transfer(c, b, a))              # 参数传错了：运行时照样跑
print(type(a))                        # NewType 在运行时就是原来的 str
```

实际输出：

```
acme: acc-1->acc-2
acc-1: acme->acc-2
<class 'str'>
```

把上面的代码存成 `l3.py` 交给 mypy，第 11 行（`transfer(c, b, a)`）的检查结果：

```
l3.py:11: error: Argument 1 to "transfer" has incompatible type "ClientId"; expected "AccountId"  [arg-type]
l3.py:11: error: Argument 3 to "transfer" has incompatible type "AccountId"; expected "ClientId"  [arg-type]
```

**为什么。** 第二行输出是真正的 bug：运行时不报错，把调用方当成了账户。不跑检查器的环境里 `NewType` 没有保护，所以它要和 CI 里的类型检查一起用才算数。

**代价。** 边界上要显式包装：从 JSON 读出的 `str` 先 `AccountId(raw)`，这个动作也是个提醒点：在此做格式校验。需要运行时区分，或者要带校验与方法：用冻结数据类包一层。
