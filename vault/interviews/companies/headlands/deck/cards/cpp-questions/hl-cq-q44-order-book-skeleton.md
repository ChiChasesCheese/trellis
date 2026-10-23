---
id: hl-cq-q44-order-book-skeleton
node: cpp-questions.k-experience
type: qa
step: 8
---
## Q
典型的现场骨架：命令解析 + 订单簿。订单、买盘、卖盘各用什么数据结构？输入 `ADD 1 B 100 10 / ADD 2 B 101 5 / ADD 3 S 105 7 / CANCEL 2 / ADD 4 S 103 1 / BEST` 输出什么？

## A
- `unordered_map` 存 订单 id → 订单。
- 买盘 `std::map<int,int,std::greater<int>>`（最高价在前）；卖盘 `std::map<int,int>`（最低价在前）。
- `adjust` 用泛型 lambda 同时处理两种 map。
- 输出：
```
cancel 2 ok
best bid 100, best ask 103
```
（订单 2 被撤销后，最高买价是 100；最低卖价是 103。）
