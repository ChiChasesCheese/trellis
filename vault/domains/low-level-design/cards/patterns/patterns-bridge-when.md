---
id: patterns-bridge-when
node: patterns.structural
type: qa
step: 3
---
## Q
你有 `Shape` × `Renderer` 两个维度，继承会导致 `VectorCircle`、`RasterCircle`、`VectorSquare`、`RasterSquare` 组合爆炸，哪个模式能解决？它和 Adapter 有什么不同？

## A
**Bridge**：把两个各自独立变化的维度拆成两个类层次，用组合（composition）连接——`Shape` 持有一个 `Renderer`。类数从 n×m 降到 n+m，两个维度可以各自独立扩展。

```python
class Renderer:
    def render_circle(self, radius: float) -> None: ...

class Shape:
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

class Circle(Shape):
    def draw(self, radius: float) -> None:
        self.renderer.render_circle(radius)
```

Adapter 改的是一个类的接口，让它符合调用方已有的期望；Bridge 分离的是两个都会独立变化的维度。两者都用组合实现，但要解决的问题不同。
