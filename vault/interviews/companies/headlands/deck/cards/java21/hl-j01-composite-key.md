---
id: hl-j01-composite-key
node: java21.j01-record
type: qa
step: 21
---
## Q
需要按 `(symbol, side)` 分组聚合数量时，用字符串 `symbol + "|" + side` 当 Map key，和 `record BookKey(String symbol, Side side)` 相比差在哪？

## A
字符串拼接：丢失类型；`symbol` 本身含 `|` 就会串；字段顺序变了编译器不管；还要自己解析回来。

`record BookKey(String symbol, Side side) {}` 是真正的类型：访问器有类型，`equals` / `hashCode` 自动正确，全程受编译器检查。

```java
qtyByBook.merge(new BookKey(f.symbol(), f.side()), f.qty(), Long::sum);
```
只有 key 要序列化成文本（如 Redis key）时字符串才有理由，且只在边界处拼。
