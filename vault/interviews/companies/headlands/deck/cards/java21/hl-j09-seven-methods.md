---
id: hl-j09-seven-methods
node: java21.j09-sequenced-collections
type: qa
step: 6
---
## Q
补全代码：写出 `SequencedCollection<E>` 接口的七个方法签名。

## A
```java
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();   // 倒序视图（不拷贝）
    void addFirst(E e);   void addLast(E e);
    E getFirst();         E getLast();
    E removeFirst();      E removeLast();
}
```
七个方法：`reversed`、`addFirst`、`addLast`、`getFirst`、`getLast`、`removeFirst`、`removeLast`。
