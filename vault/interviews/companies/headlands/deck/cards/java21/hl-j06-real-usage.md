---
id: hl-j06-real-usage
node: java21.j06-instanceof-pattern
type: qa
step: 20
---
## Q
真实代码里 `instanceof` 模式用在哪些地方？`mapMulti` 的惯用写法是什么样？

## A
用得不多，因为按类型分派的场合都被 `switch` 模式接管了。真实用到的：

- 事件流过滤：`if (e instanceof Rejected(var id, var why)) { throw ... }`（record 模式）；
- `mapMulti` 里"只挑某一种"：
  ```java
  events.stream().<Trade>mapMulti((e, sink) -> {
      if (e instanceof Trade t) sink.accept(t);
  }).toList();
  ```
  `mapMulti` 把每个元素映射成 0..n 个输出，靠 `sink.accept` 发出；
- 三元运算符里：`e instanceof MergeException me ? me : new MergeException(-1, e)`，`me` 只在"是"的分支可用；
- 只有类型检查没有绑定变量的旧式写法依然合法。
