---
id: hl-cx-triangle-count-q2
node: foundations.complexity
type: qa
step: 47
---
## Q
下面代码内层 `count++` 一共执行多少次？复杂度是什么？n = 4 时是多少？

```java
for (int i = 0; i < n; i++)
    for (int j = i; j < n; j++)
        count++;
```

## A
i = 0 时内层 n 次，i = 1 时 n−1 次，……，i = n−1 时 1 次，总数 n + (n−1) + … + 1 = **n(n+1)/2**，复杂度 O(n²)。n = 4 时 4 + 3 + 2 + 1 = **10**。
