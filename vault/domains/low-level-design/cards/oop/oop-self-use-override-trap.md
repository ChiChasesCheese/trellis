---
id: oop-self-use-override-trap
node: oop.pillars
type: qa
---
## Q
```java
class CountingSet<E> extends HashSet<E> {
  int added = 0;
  public boolean add(E e) { added++; return super.add(e); }
  public boolean addAll(Collection<? extends E> c) { added += c.size(); return super.addAll(c); }
}
```
`addAll` 加 3 个元素，报出来是 6。为什么？这件事关于继承说明了什么？

## A
`HashSet.addAll` 的实现方式是在循环里调用 `this.add()` —— 这叫 **self-use（自用）**。被覆盖的 `add` 会执行并再数一遍，于是每个元素都被计了两次。

子类之所以坏掉，是因为它依赖了基类*未被规定的内部细节*。两个后果：

- 一个基类只有在**把自己的 self-use 写进文档**时才可以被安全继承（Java 的 "@implSpec / this implementation calls…"），而这份文档从此就把基类的内部实现永久冻住了。
- 构造函数里有同样的陷阱：基类构造函数调用可被覆盖的方法，那个覆盖会在子类字段初始化**之前**执行。

这里的修法：改用组合 —— 包一个 `Set` 并转发。
