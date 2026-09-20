---
id: oop-getter-collection-leak
node: oop.pillars
type: qa
---
## Q
```java
class Floor {
  private final List<Spot> spots;
  public List<Spot> getSpots() { return spots; }
}
```
字段是 `private final`。解释封装为什么仍然被破坏了，并按优先级给出三种修法。

## A
`final` 保护的是**引用**，不是内容 —— 调用方拿到的是那个活着的 list，可以 `add`/`clear`，绕开 `Floor` 强制的每一条规则。**入口方向**也有同样的泄漏：构造函数直接存下调用方传进来的 list，调用方之后照样能继续改它。

1. **根本不要暴露** —— 改成暴露操作：`floor.findFreeSpot(size)`。
2. 返回**不可变视图**（`List.copyOf` / `Collections.unmodifiableList`），并在构造函数里做防御性拷贝。
3. 只有当调用方确实需要任意遍历时，才暴露 stream/iterator。

getter 返回可变的内部结构（集合、`Date`、数组）是 code review 中最常见的封装泄漏。
