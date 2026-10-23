---
id: hl-j16-release-acquire
node: java21.j16-concurrency-primitives
type: qa
step: 15
---
## Q
解释 `setRelease` 与 `getAcquire`，并写出用它们发布 `price`、`qty` 的写者和读者代码。

## A
- `setRelease(x)`：**之前**的所有读写不会被重排到这次写之后，是「向上」的单向门。
- `getAcquire()`：**之后**的所有读写不会被重排到这次读之前，是「向下」的单向门。
- B 的 `getAcquire` 读到 A 的 `setRelease` 写的值时，A 在 release 之前写的一切，B 在 acquire 之后都能看到，这就是**发布—订阅**。

```java
// 写者                          // 读者
price = p; qty = q;             if ((int) READY.getAcquire(this) == 1) {
READY.setRelease(this, 1);          use(price, qty);   // 一定看到 p 和 q
                                }
```
