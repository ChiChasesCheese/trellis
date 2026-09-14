---
id: patterns-composite-when
node: patterns.structural
type: qa
---
## Q
What problem shape calls for Composite, and what's the design tension inside the pattern?

## A
Use it when clients must treat **individual objects and groups of them uniformly** through one interface — the domain is a part-whole **tree**: file/directory, UI widget/container, single item/bundle in an order, expression AST.

```java
interface Node { long size(); }        // File returns bytes;
class Dir implements Node {            // Dir sums children — caller can't tell
    long size() { return children.stream().mapToLong(Node::size).sum(); }
}
```

Tension: put child-management (`add`/`remove`) on the common interface and leaves get meaningless methods (**transparency**, GoF's choice); put it only on the composite and clients must downcast (**safety**). Say which you chose and why.

Don't force it when the "hierarchy" is only ever one level deep — a plain list is simpler.

## Q zh
什么问题形状需要 Composite，模式内部的设计张力是什么？

## A zh
当客户端必须通过一个接口统一对待**单个对象和对象组**时使用它——域是一个部分-整体**树**：文件/目录、UI 组件/容器、单项/订单中的包、表达式 AST。

```java
interface Node { long size(); }        // 文件返回字节；
class Dir implements Node {            // 目录求和子元素——调用者看不出区别
    long size() { return children.stream().mapToLong(Node::size).sum(); }
```

张力：Composite 要求叶子和节点有通用接口，所以有些方法在叶子上没意义（如「添加子元素」）。
