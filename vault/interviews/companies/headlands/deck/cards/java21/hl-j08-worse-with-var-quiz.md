---
id: hl-j08-worse-with-var-quiz
node: java21.j08-var
type: qa
step: 25
---
## Q
面试追问：举一个"用 `var` 反而更糟"的例子，并给出改法。

## A
- `var total = 0; ... total += qty;`（`qty` 是 `long`）：`total` 是 `int`，溢出风险被推导悄悄隐藏，改 `long total = 0;`。
- `var result = repo.find(id);`：读者看不出是 `Optional<Order>` 还是 `Order`——显式写类型，或把方法名改明确（如 `findOrder`）。
- `var list = new ArrayList<>();`：得到 `ArrayList<Object>`，改 `new ArrayList<Fill>()`。
