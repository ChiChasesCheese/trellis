---
id: hl-j09-reversed-view
node: java21.j09-sequenced-collections
type: qa
step: 9
---
## Q
`list.reversed()` 是拷贝还是视图？举一个能证明的操作，并写出结果。

## A
是**视图**（view）：O(1) 创建，不复制数据，读写都穿透到原集合。

```java
List<String> list = new ArrayList<>(List.of("a", "b", "c"));
List<String> rev = list.reversed();     // [c, b, a]
rev.addFirst("LAST");                    // list 变成 [a, b, c, LAST]：写穿到原列表末尾
list.add("tail");                        // rev 立刻变成 [tail, LAST, c, b, a]
```
修改视图 = 修改原集合，修改原集合视图也立刻看得到。
