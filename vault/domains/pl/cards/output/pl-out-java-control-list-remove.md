---
id: pl-out-java-control-list-remove
node: output.java-control
type: qa
step: 4
---
## Q
**remove 的两个重载**｜读代码说输出

```java
public class Main { public static void main(String[] x) {
    List<Integer> l = new ArrayList<>(List.of(10, 20, 1, 2));
    l.remove(1);
    System.out.println(l);
    l.remove(Integer.valueOf(1));
    System.out.println(l);
    List<String> s = new ArrayList<>(List.of("a", "b", "c"));
    for (String e : s) if (e.equals("b")) s.remove(e);
    System.out.println(s);
    List<String> t = new ArrayList<>(List.of("a", "b", "c"));
    try { for (String e : t) if (e.equals("a")) t.remove(e); }
    catch (ConcurrentModificationException e) { System.out.println("CME"); }
} }
```

输出什么？

## A
**输出。**
```
[10, 1, 2]
[10, 2]
[a, c]
CME
```

**为什么。**
- `List<Integer>` 有 `remove(int index)` 和 `remove(Object)` 两个重载。传 int 字面量精确匹配前者，删的是下标 1 的 20；要按值删，必须装箱 `Integer.valueOf(1)`。
- for-each 底层是迭代器，`ArrayList` 的迭代器带修改计数 modCount；遍历中直接 `list.remove` 改了结构，下一次 `next()` 发现计数变了，抛 `ConcurrentModificationException`。
- 删倒数第二个元素时是例外：删完 size 是 2、游标也是 2，`hasNext()` 直接返回 false，循环悄悄结束，所以第三行是 [a, c]。

**语言为什么这样设计。**
- 迭代器的快速失败（fail-fast）只是尽力检测，文档明说不能依赖；用一个计数器而不是加锁，是为了让普通的单线程遍历零成本。
- 两个 `remove` 重载在 Java 5 加入自动装箱前就存在，为兼容不能改名；Python 用 `pop(i)` 与 `remove(x)` 两个名字，没有这个坑。

**怎么写才对。**
```java
list.removeIf(e -> e.equals("b"));       // 遍历中安全删除
list.remove(Integer.valueOf(1));          // 按值删
```

**面试里一句话。**
Mutating a list inside a for-each throws ConcurrentModificationException, except when the loop happens to end first; use removeIf.
