---
id: patterns-composite-when
node: patterns.structural
type: qa
---
## Q
什么问题形状需要 Composite，模式内部的设计张力是什么？

## A
当客户端必须通过一个接口统一对待**单个对象和对象组**时使用它——域是一个部分-整体**树**：文件/目录、UI 组件/容器、单项/订单中的包、表达式 AST。

```java
interface Node { long size(); }        // 文件返回字节；
class Dir implements Node {            // 目录求和子元素——调用者看不出区别
    long size() { return children.stream().mapToLong(Node::size).sum(); }
```

张力：Composite 要求叶子和节点有通用接口，所以有些方法在叶子上没意义（如「添加子元素」）。
