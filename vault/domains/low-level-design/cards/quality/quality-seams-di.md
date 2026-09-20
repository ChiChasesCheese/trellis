---
id: quality-seams-di
node: quality.testability
type: qa
---
## Q
可测性意义上的 "seam（接缝）"是什么，为什么方法内部的 `new` 会毁掉一个接缝？

## A
**Seam**（Feathers 的定义）：一个**不修改被测代码就能改变程序行为**的位置 —— 也就是协作者可以被替换的地方。

```java
class OrderService {
    void place(Order o) {
        var gw = new StripeGateway();   // 没有接缝：测试必须真的打 Stripe
        ...
```

`new`（和静态调用一样）在使用点把具体类硬焊死了 —— 不存在任何可替换的位置。修法：通过**构造函数**以接口形式接收依赖；测试传入 fake，生产环境的装配发生在 composition root。

经验法则：一个类可以 `new` 自己的**值对象和数据结构**，但凡是涉及 I/O、时间、随机性、或者本身有值得被 fake 的行为的东西，都应该注入进来。
