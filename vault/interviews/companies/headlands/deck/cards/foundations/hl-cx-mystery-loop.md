---
id: hl-cx-mystery-loop
node: foundations.complexity
type: qa
step: 7
---
## Q
下面代码的复杂度是多少？n = 8 和 n = 16 时 `steps` 各是多少？

```java
for (int i = 1; i <= n; i *= 2)
    for (int j = 0; j < n; j++) steps++;
```

## A
外层 `i` 每次翻倍（1, 2, 4, 8, …），从 1 涨到超过 n 需要 ⌊log₂ n⌋ + 1 轮；内层每轮固定 n 步。所以 steps = n × (⌊log₂ n⌋ + 1)，复杂度 **O(n log n)**。

- n = 8：i = 1, 2, 4, 8 共 4 轮，每轮 8 步，steps = **32**。
- n = 16：i = 1, 2, 4, 8, 16 共 5 轮，每轮 16 步，steps = **80**。
