---
id: hl-cx-pitfall-hidden-loops
node: foundations.complexity
type: qa
step: 39
---
## Q
什么是复杂度分析里的「隐藏循环」？下面循环的复杂度是多少，怎么改？

```java
for (int q : queries)            // n 次
    if (list.contains(q)) hits++;
```

## A
`list.contains(q)` 对 `List` 是 O(list.size())，循环里每次调用就是隐藏的内层循环，整体 **O(n × m)**（m 是 list 大小），不是 O(n)。

改法：把 `list` 换成 `HashSet<Integer>`，`contains` 平均 O(1)，整体 O(n + m)。

同类隐藏循环：循环里 `s += x` 拼接字符串，每次复制整个字符串，整体 O(n²)，要用 `StringBuilder`。「我只用了一个循环所以 O(n)」是错的，要看循环体每次做什么。
