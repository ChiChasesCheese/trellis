---
id: patterns-flyweight-when
node: patterns.structural
type: qa
---
## Q
Flyweight: what state do you split, and what constraint makes the shared part safe?

## A
Split object state into:

- **Intrinsic** — identical across many instances (glyph shape, tree species mesh/texture, chess piece type). Stored once, **shared** via a factory/cache.
- **Extrinsic** — varies per use (position, color, owner). Passed in by the caller at each operation: `species.render(x, y)`.

The shared intrinsic part must be **immutable** — otherwise one user's mutation corrupts every other user.

Use only when instance counts are large enough that memory actually hurts (millions of particles/glyphs/cells); for ordinary object counts it's needless indirection. `Integer.valueOf` caching and string interning are the stock real-world examples.

## Q zh
什么时候 Flyweight 值得麻烦？成本-收益是什么？

## A zh
当你有**大量相似对象**且内存是瓶颈时。Flyweight 把**共享的、不可变的状态**（intrinsic，如字符编码）与**每个对象的、可变的**状态（extrinsic，如位置、颜色）分离。

成本：
- 代码复杂性：两个状态流、工厂池、extrinsic 状态管理。
- 查询缓存（`FlyweightFactory.get(key)` 比 `new` 快但不是免费的）。

收益：
- 内存：1000 个文本编辑器中的相同 `Character` 对象只存储一次。
- GC 压力：更少的对象 = 更少的 GC 停顿。

经验法则：> 10k 个对象且共享 > 80% 时考虑。
