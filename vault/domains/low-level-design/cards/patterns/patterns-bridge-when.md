---
id: patterns-bridge-when
node: patterns.structural
type: qa
---
## Q
你有 `Shape` × `Renderer`，继承导致了 `VectorCircle`、`RasterCircle`、`VectorSquare`、`RasterSquare`……哪个模式能解决，它与 adapter 有什么不同？

## A
**Bridge**：把两个独立的维度分成两个层次，通过**组合**连接它们——`Circle` 持有一个 `Renderer`。类数从 *n×m* 子类下降到 *n+m* 类，每个维度独立变化。

```java
abstract class Shape { protected final Renderer r; ... }
class Circle extends Shape { void draw() { r.renderCircle(radius); } }
```

Adapter 改变一个类的接口以匹配客户端期望；Bridge 分离两个变化的维度。
