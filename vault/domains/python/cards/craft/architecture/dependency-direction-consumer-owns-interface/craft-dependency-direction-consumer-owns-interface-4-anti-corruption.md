---
id: craft-dependency-direction-consumer-owns-interface-4-anti-corruption
node: craft.architecture.dependency-direction-consumer-owns-interface
type: qa
step: 4
---
## Q
**依赖方向 · 从一个 Protocol 到六边形架构与防腐层**｜架构

下单流程里的 `PaymentGateway` 是单进程里的一个 Protocol。接入真实支付供应商时，对方的 SDK 有自己的字段名（`amt_cents`）、状态码（`card_declined`）和异常。怎样不让这些东西渗进核心代码？在系统设计层面这叫什么？

## A
**要点。** 同一个想法放大就是六边形架构（hexagonal architecture，又叫 ports and adapters）：核心定义端口（port，即 Protocol），外部系统各写一个适配器（adapter）。适配器负责翻译命名、错误、单位，这一层又叫防腐层（anti-corruption layer）：供应商的概念到此为止，核心只认识自己的异常和类型。

```python
class PaymentDeclined(Exception): ...            # 消费者自己的异常

class PaymentGateway(Protocol):                  # 消费者（下单流程）定义的接口
    def charge(self, idempotency_key: str, amount: int) -> str: ...

class VendorSdk:                         # 外部服务：形状和命名是别人的
    def create_charge(self, *, amt_cents: int, idem: str) -> dict:
        return {"status": "card_declined", "id": None}   # 桩：恒拒绝

class VendorAdapter:                     # 防腐层：翻译成消费者的语言
    def __init__(self, sdk: VendorSdk) -> None:
        self._sdk = sdk
    def charge(self, idempotency_key: str, amount: int) -> str:
        r = self._sdk.create_charge(amt_cents=amount, idem=idempotency_key)
        if r["status"] != "ok":
            raise PaymentDeclined(r["status"])   # 供应商状态码不漏进核心
        return r["id"]

gateway: PaymentGateway = VendorAdapter(VendorSdk())
try:
    gateway.charge("order-1", 500)
except PaymentDeclined as e:
    print("核心只认识 PaymentDeclined:", e)
```

实际输出：

```
核心只认识 PaymentDeclined: card_declined
```

**为什么。** 换供应商只换适配器；供应商升级字段，只改适配器一处，核心的测试不受影响。

**代价。** 每多一个外部系统就多一层翻译代码，翻译不好还会丢信息（比如把所有失败都映射成同一个异常，调用方就分不清可重试和不可重试）；小项目且只对接一家时，可以先不分层。

**信号。** 核心代码里出现供应商的字段名、状态码字符串或 SDK 异常类型，就是漏了。
