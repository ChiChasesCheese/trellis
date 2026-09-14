---
id: patterns-bridge-when
node: patterns.structural
type: qa
---
## Q
You have `Shape` × `Renderer` and inheritance is producing `VectorCircle`, `RasterCircle`, `VectorSquare`, `RasterSquare`... Which pattern fixes this, and how is it different from adapter?

## A
**Bridge**: split the two independent dimensions into two hierarchies and connect them by **composition** — `Circle` holds a `Renderer`. Class count drops from *n×m* subclasses to *n+m* classes, and each dimension varies independently.

```java
abstract class Shape { protected final Renderer r; ... }
class Circle extends Shape { void draw() { r.renderCircle(radius); } }
```

Vs adapter: **bridge is designed up front** so abstraction and implementation can evolve separately; **adapter is retrofitted** to make already-incompatible things work together. Same "interface + impl" skeleton, opposite point in the lifecycle.

Tell: the phrase "every combination of A and B" in requirements.

## Q zh
你有 `Shape` × `Renderer`，继承导致了 `VectorCircle`、`RasterCircle`、`VectorSquare`、`RasterSquare`……哪个模式能解决，它与 adapter 有什么不同？

## A zh
**Bridge**：把两个独立的维度分成两个层次，通过**组合**连接它们——`Circle` 持有一个 `Renderer`。类数从 *n×m* 子类下降到 *n+m* 类，每个维度独立变化。

```java
abstract class Shape { protected final Renderer r; ... }
class Circle extends Shape { void draw() { r.renderCircle(radius); } }
```

Adapter 改变一个类的接口以匹配客户端期望；Bridge 分离两个变化的维度。
