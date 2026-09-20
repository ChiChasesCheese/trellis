---
id: concurrency-double-checked-locking
node: concurrency.patterns
type: qa
---
## Q
```java
if (instance == null) {
    synchronized (Lock.class) {
        if (instance == null) instance = new Expensive();
    }
}
return instance;
```
这段双重检查锁还有什么问题，两种正确的替代写法是什么？

## A
没有 `volatile` 的话，`instance = new Expensive()` 这次写可能被**重排序**：引用在构造函数完成之前就被发布出去了。于是*第一次*（没加锁的）检查可能看到非 null，然后返回一个**构造了一半的对象**。

- 修法：把 `instance` 声明为 **`volatile`**（volatile 的写→读禁止那种重排序）。
- 在 Java 里更好的做法：**holder class 惯用法**（`static class H { static final Expensive I = new Expensive(); }`）—— 类加载器免费提供了延迟初始化加安全性，一行加锁代码都不用写。`enum` 单例同样可行。
