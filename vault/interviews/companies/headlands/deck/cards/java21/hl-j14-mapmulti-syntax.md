---
id: hl-j14-mapmulti-syntax
node: java21.j14-stream-api
type: qa
step: 9
---
## Q
`Stream.mapMulti` 的签名形态是什么？写出「从事件流里只挑出 `qty > 0` 的 `Fill`」的代码，并解释 `sink` 和 `<Fill>`。

## A
```java
List<Fill> fills = events.stream()
    .<Fill>mapMulti((e, sink) -> {
        if (e instanceof Fill f && f.qty() > 0) sink.accept(f);
    })
    .toList();
```
- lambda 参数是 `(元素, sink)`：`sink` 是 `Consumer`，调几次 `accept` 就产出几个元素（0 个或多个）。
- `<Fill>` 是**显式类型参数**：lambda 没有返回值，编译器推不出输出元素类型，不写就是 `Object`。
- 实现上每个元素调一次你的 lambda，`sink` 就是下游的 `Sink`，不建中间 `Stream`。
