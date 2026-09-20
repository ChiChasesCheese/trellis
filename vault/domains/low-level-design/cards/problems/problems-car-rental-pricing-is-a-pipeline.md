---
id: problems-car-rental-pricing-is-a-pipeline
node: problems.booking.car-rental
type: qa
step: 8
tags: [grown]
---
## Q
租车系统（Car Rental）的报价包含车型基础价 × 时长、异地还车附加费、保险等加购项、会员折扣，而且随时要加「周末加价」「机场取车费」。为什么不该用 `PricingStrategy` 抽象基类加一堆子类？

## A
因为定价不是「**几选一**」，而是「**几项相加**」——策略模式（Strategy）解决的是前者。

用抽象基类你会立刻需要一个 `CompositePricingStrategy` 去组合它们；又因为会员折扣要对**小计**打折，还得给接口加一个 `subtotal` 参数。最后得到的就是一串函数，只不过外面套了四层类。

Python 里的自然形态是一串可调用对象，按顺序跑：

```python
PriceComponent = Callable[[RentalRequest, int], Charge | None]

def one_way_fee(amount: int) -> PriceComponent:
    def component(request: RentalRequest, subtotal: int) -> Charge | None:
        return Charge("one_way", amount) if request.one_way else None
    return component
```

策略只有一个方法且不共享状态时，它**就是**一个函数；需要参数就用闭包。两个细节：签名里**没有** `Fleet`，所以定价函数绕不过车队的锁去读内部状态；返回 `Charge | None` 而不是 `int`，因为报价必须是分项的——只给一个总数的设计在第一次客诉时就会崩。金额一律用整数分，不用 `float`。
