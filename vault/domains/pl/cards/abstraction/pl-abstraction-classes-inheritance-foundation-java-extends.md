---
id: pl-abstraction-classes-inheritance-foundation-java-extends
node: abstraction.classes-inheritance
type: qa
step: 2
---
## Q
Java 的 `extends`、覆写（override）、`super` 和抽象类各是什么？一个小例子里调用 `speak()` 时到底执行了哪段代码？

## A
心智模型：**子类是「父类 + 增量」**。`extends` 让子类对象自带父类的字段和方法；子类可以**覆写**（重新定义同签名的方法）来替换行为；`super(...)` / `super.m()` 调用父类的版本；`abstract` 方法只有签名，要求子类必须实现。一个类只能 `extends` 一个类。

```java
abstract class Animal {
    String name; Animal(String n) { name = n; }
    abstract String sound();                              // 子类必须实现
    String speak() { return name + " says " + sound(); }  // 通用流程
}
class Dog extends Animal {
    Dog(String n) { super(n); }
    @Override String sound() { return "woof"; }
}
Animal x = new Dog("rex");
x.speak();   // "rex says woof"
```

`x` 的声明类型是 `Animal`，实际对象是 `Dog`。`speak()` 在 `Animal` 里写一次，内部调用 `sound()` 时按**对象的实际类型**选择，因此执行的是 `Dog.sound`。这种「父类写骨架、子类填空」的写法叫模板方法（template method），是继承最典型的用途；子类对象能当父类用（`Animal x = new Dog(...)`）则是子类型多态。
