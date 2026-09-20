---
nodes: [problems.machines.coffee-machine]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/coffee-vending-machine.md
---
# awesome-low-level-design — Designing a Coffee Vending Machine

值得读：六种语言（含 Python）并排给出同一份设计，实体是 `Coffee`（名字、价格、配方）、
`Ingredient`（带一个加了同步的数量更新方法）、`Payment`、`CoffeeMachine`（Singleton），
并用线程池模拟并发请求，可以用来核对需求项有没有漏。本题解在三处明确不同：它把原子性落在
**单个原料**上（每个 `Ingredient` 自己同步），而一份配方要同时动好几种原料，真正需要原子的
是整份扣减——否则就会出现"扣了牛奶没扣咖啡"的半杯；它的 `CoffeeMachine` 是单例，而测试必须
能同时造出两台互不干扰的机器；它没有讨论临界区的边界（冲煮要不要在锁里），而那恰恰是这道题
唯一真正的考点。它还把支付和找零一起放了进来，本文把那部分留给售货机那道题。
