---
id: quality-constructor-injection
node: quality.testability
type: qa
step: 2
---
## Q
为什么构造函数注入（constructor injection）优于事后靠属性赋值来"装配"依赖？

## A
```python
class OrderService:
    def __init__(self, repo: OrderRepository, clock: Clock):
        self._repo = repo
        self._clock = clock
```
第一，对象一旦构造完成就是完整可用的——不存在"已经 new 出来了，但还没接好线"这种中间态；靠属性赋值装配的对象，调用方必须自己记得按正确顺序把每个依赖都设置一遍，漏了哪个只有运行时才会报错。第二，构造函数的参数列表就是一份诚实的依赖清单，全部摆在一个签名里——一个要求六个协作者的构造函数看着丑,但这正是好事：它让"这个类做的事太多"这条设计问题无处遁形,而分散的属性赋值会把同样的问题悄悄藏起来。

第三，测试不需要任何框架或反射：`OrderService(FakeRepo(), FixedClock(...))` 就是一次普通的函数调用。属性注入仅剩的合理场景是真正**可选**的依赖，或者需要打破循环依赖——两者都少见，而循环依赖本身通常是该消灭的设计问题，不是该迁就的现状。
