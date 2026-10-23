---
id: hl-j01-defensive-copy
node: java21.j01-record
type: qa
step: 12
---
## Q
`record Basket(String name, List<Order> orders)` 的组件是集合时，如何防止调用方事后改动里面的内容？写出代码。

## A
```java
record Basket(String name, List<Order> orders) {
    Basket {
        orders = List.copyOf(orders);   // 不可修改的拷贝；null 元素抛 NPE
    }
}
```
不拷贝的话，调用方仍持有原 `ArrayList`，随时能往里加东西，`Basket` 就被悄悄改了。

拷贝后，再往原列表加一单，`basket.orders().size()` 仍不变，`basket.orders()` 本身也不可修改。这叫**防御性拷贝**（defensive copy）。
