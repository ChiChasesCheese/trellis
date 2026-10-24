---
id: pl-eng-apidesign-pitfall-leaked-state
node: engineering.api-design
type: qa
step: 10
---
## Q
一个类的 getter 直接返回内部的集合会出什么问题？Java 的 `List` 和 Go 的切片分别怎样“泄漏”内部状态，怎么修？

## A
封装的目的是让对象自己保证不变式（比如“只能通过 `add` 加商品”）。但如果 getter 把**内部可变对象的引用**交出去，调用者就可以绕过所有方法直接改它。

**Java**：
```java
List<String> items() { return items; }                  // leaks the internal list
List<String> safeItems() { return List.copyOf(items); } // immutable snapshot
// c.add("book"); c.items().clear(); -> after caller clear: []
// c.safeItems().add("x")            -> UnsupportedOperationException
```
调用者拿到的是同一个 `ArrayList`，`clear()` 之后购物车被清空了，而 `add` 里的任何校验、日志、事件通知都被绕过了。`List.copyOf` 返回不可变副本，修改会直接抛 `UnsupportedOperationException`。

**Go**：切片是（指针、长度、容量）三元组，返回切片等于交出底层数组的访问权：
```go
func (c *Cart) Items() []string { return c.items }
got := c.Items(); got[0] = "HACKED"
fmt.Println(c.items)   // [HACKED pen]
```
修复是返回副本：`slices.Clone(c.items)`；Go 里 map 同样是引用类型。**Python** 的列表、字典也一样；**Rust** 在这里最安全：返回 `&[T]`（只读借用）就不能被修改，要修改必须有 `&mut self`，编译器保证了封装。

**两个方向的泄漏**：
1. **输出**：getter 返回内部可变对象（上面这些）；
2. **输入**：构造器接受调用者传来的集合并直接保存，之后调用者继续修改自己手里的那个集合，对象内部也跟着变。修复：保存时防御性复制（`List.copyOf(input)`、`slices.Clone`、`list(input)`）。

**做法**：
- Java 用不可变类型（`record`、`List.of`、`copyOf`）；Go 在文档里写明“返回的切片调用者不得修改”，或直接返回副本，热点路径再优化；Python 返回 `tuple` 或拷贝；
- 复制有成本：很大的集合可以返回只读视图（`Collections.unmodifiableList` 是视图，不复制，但底层变化仍会可见）。
