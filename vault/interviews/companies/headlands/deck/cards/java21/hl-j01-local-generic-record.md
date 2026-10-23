---
id: hl-j01-local-generic-record
node: java21.j01-record
type: qa
step: 13
---
## Q
`record` 能不能声明在方法内部？能不能带泛型？各写一个例子，并说明局部 `record` 的特点。

## A
可以。**局部 record**（local record）声明在方法内部，**隐式 static**，只在该方法内可见，适合"这个方法里临时要个小结构"：

```java
static long topNotional(List<String> lines) {
    record Row(String sym, long px, long qty) {}
    return lines.stream().map(l -> l.split(","))
        .map(t -> new Row(t[0], Long.parseLong(t[1]), Long.parseLong(t[2])))
        .mapToLong(r -> r.px() * r.qty()).max().orElse(0);
}
```
**泛型 record**：`record Tagged<T>(T value, boolean valid) {}`。
