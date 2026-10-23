---
id: hl-j02-when-each-modifier
node: java21.j02-sealed
type: qa
step: 5
---
## Q
`final`、`sealed`、`non-sealed` 三个子类修饰符分别在什么场景选？用 `Instrument` 层级写出一个同时包含三种的例子。

## A
- `final`：最常见，叶子类型。
- `sealed`：层级有多层，如"Update 指令"下面还有 15 种。
- `non-sealed`：想留一个扩展点，如"用户自定义指令"。

```java
sealed static abstract class Instrument { abstract String ticker(); }
static final class Stock extends Instrument { ... }                // final
static sealed abstract class Option extends Instrument { ... }     // 继续封闭
static final class CallOption extends Option {}
static final class PutOption extends Option {}
static non-sealed class Custom extends Instrument { ... }          // 重新开放
static class UserDefined extends Custom {}                         // 合法
```
