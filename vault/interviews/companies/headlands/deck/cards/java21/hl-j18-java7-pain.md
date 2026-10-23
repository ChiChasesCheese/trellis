---
id: hl-j18-java7-pain
node: java21.j18-comparators-interfaces
type: qa
step: 2
---
## Q
Java 7 写「价格降序、时间升序、id 升序」的比较器有哪三个痛点？

## A
```java
Collections.sort(orders, new Comparator<Order>() {
    @Override public int compare(Order a, Order b) {
        int c = Long.compare(b.px, a.px);       // 降序：把 a、b 对调
        if (c != 0) return c;
        c = Long.compare(a.ts, b.ts);
        if (c != 0) return c;
        return Long.compare(a.id, b.id);
    }
});
```
1. **啰嗦**：6 行匿名类只为说那一句话。
2. **容易写错**：降序靠「把 a、b 对调」心算；每层 tie-break 都要 `if (c != 0) return c;`，漏一层就悄悄变成不稳定的排序。
3. **经典 bug：用减法比较** `return a - b;`，会溢出，永远用 `Integer.compare` / `Long.compare`。
