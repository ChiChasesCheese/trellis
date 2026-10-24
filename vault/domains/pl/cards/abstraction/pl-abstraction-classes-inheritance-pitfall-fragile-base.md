---
id: pl-abstraction-classes-inheritance-pitfall-fragile-base
node: abstraction.classes-inheritance
type: qa
step: 9
---
## Q
什么是脆弱基类问题（fragile base class）？一个统计 `HashSet` 添加次数的子类为什么会数错？

## A
子类依赖了父类的**实现细节**，父类的内部调用关系一变（或者本来就和你想象的不同），子类就悄悄出错。

```java
class CountingSet<E> extends HashSet<E> {
    int added = 0;
    @Override public boolean add(E e) { added++; return super.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) {
        added += c.size(); return super.addAll(c);
    }
}
// addAll(List.of("a","b","c")) 之后：
// 输出 6 counted, 3 stored
```

原因：`HashSet.addAll` 继承自 `AbstractCollection`，它的实现内部会逐个调用 `this.add(e)`。子类的 `addAll` 先加了 3，随后 `add` 又被调用 3 次再加 3，一共 6。如果 JDK 将来把 `addAll` 改成直接批量插入，计数又会变成 3；两种实现都符合 `HashSet` 的公开契约，子类却在不同版本给出不同答案。

修法是**组合 + 转发**：持有一个 `Set<E>` 字段，自己实现 `add` / `addAll`，只调用字段的公开方法。这样只依赖契约，不依赖实现。

规律：只要子类覆写了「父类内部也会调用」的方法，就有这个风险；而这种自用关系在文档里常常没有写。这正是 Go 与 Rust 放弃实现继承的核心理由。C++ 里除了这一类，还有它特有的两种基类陷阱：基类析构函数不是 `virtual`（声明后按对象实际类型调用）时，`Base* p = new Derived; delete p;` 只运行基类析构（本机输出只有 `~Base`，派生部分泄漏，标准称之为未定义行为，即不规定后果）；按值把派生对象传给基类参数会切片，`byValue(Dog)` 调到的是 `Animal::speak`（输出 `rex ...`），按引用才是 `Dog::speak`（输出 `rex woof`）。
