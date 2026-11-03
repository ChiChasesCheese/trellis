---
id: craft-interface-only-when-earned-2-function-is-enough
node: craft.architecture.interface-only-when-earned
type: qa
step: 2
---
## Q
**接口是挣来的 · 只有一个方法的角色为什么写成函数**｜架构

订座系统的超售政策、票价政策、退票政策，各自只回答一个问题。消息订阅里的处理器也只有「收下一条消息」这一个动作。把它们写成抽象基类（ABC）加若干子类，和写成函数有什么区别？什么时候函数不够用了？

## A
**要点。** 只有一个方法的角色，类型别名加普通函数就够了：不需要基类、不需要继承，带配置的政策用闭包（closure，函数里返回的函数）带着参数；测试里一个 `lambda` 就是替身。

```python
Cabin = Enum("Cabin", "ECON FIRST")
OverbookingPolicy = Callable[[Cabin, int], int]       # (舱位, 座位数) -> 超售张数

def no_overbooking(cabin: Cabin, seats: int) -> int:
    return 0

def percent_overbooking(by_cabin: dict[Cabin, int]) -> OverbookingPolicy:
    def policy(cabin: Cabin, seats: int) -> int:          # 闭包带着配置
        return seats * by_cabin.get(cabin, 0) // 100
    return policy

def authorized(cabin: Cabin, seats: int, policy: OverbookingPolicy) -> int:
    return seats + policy(cabin, seats)

print(authorized(Cabin.ECON, 100, no_overbooking))
print(authorized(Cabin.ECON, 100, percent_overbooking({Cabin.ECON: 10})))
print(authorized(Cabin.FIRST, 8, percent_overbooking({Cabin.ECON: 10})))
print(authorized(Cabin.ECON, 100, lambda c, s: 3))        # 测试里一行就能造替身
```

三个调用加一个测试替身（`lambda c, s: 3`），实际输出：

```
100
110
8
103
```

分别是：不超售的经济舱 100 座，经济舱 10% 超售得到 110，头等舱没配置所以仍是 8，替身固定加 3 得到 103。

**为什么。** 类版本要多写基类、子类、构造函数，换来的只是一次方法分派；函数版本把「是什么」直接放进类型别名，调用方用什么形式提供都行（函数、闭包、可调用对象）。

**代价。** 函数没有名字之外的结构：当政策需要多个相关方法、要在构造时校验自己的配置，或者要有多个实现共享一段代码时，就该升级成类，见下一张。
