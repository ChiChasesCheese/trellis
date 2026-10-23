---
id: hl-j01-record-as-map-key
node: java21.j01-record
type: qa
step: 19
---
## Q
两个内容相同的 `record Fill` 实例 `a`、`b`：`a.equals(b)`、`a == b`、`map.get(b)`（`a` 已 `put`）各得到什么？

## A
```java
Fill a = new Fill("AAPL", 18_950, 100);
Fill b = new Fill("AAPL", 18_950, 100);
a.equals(b);        // true，按内容比较
a == b;             // false，引用比较，两个不同对象
notes.put(a, "first");
notes.get(b);       // "first"，内容相同的另一个对象也查得到
```
对比忘了重写 `equals` / `hashCode` 的普通类，`get` 得到 `null`。`record` 的 `equals` / `hashCode` 自动配套，不会漏。
