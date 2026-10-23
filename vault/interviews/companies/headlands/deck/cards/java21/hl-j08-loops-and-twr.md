---
id: hl-j08-loops-and-twr
node: java21.j08-var
type: qa
step: 14
---
## Q
补全代码：用 `var` 写按代码分组累加数量的双层循环，以及 `try-with-resources` 读一行并转大写。遍历 `Map` 的 `e` 是什么类型？

## A
```java
var fills = new ArrayList<Fill>();
var bySymbol = new HashMap<String, List<Fill>>();
for (var f : fills) {
    bySymbol.computeIfAbsent(f.symbol, k -> new ArrayList<>()).add(f);
}
for (var e : bySymbol.entrySet()) {          // e : Map.Entry<String, List<Fill>>
    long total = 0;
    for (var f : e.getValue()) total += f.qty;
}
try (var in = new BufferedReader(new StringReader("line1\nline2"))) {
    var line = in.readLine();                 // String
    System.out.println(line.toUpperCase());
}
```
整个 `Map.Entry<String, List<Fill>> e` 不用写，且数值变量 `total` 仍显式写 `long`。
