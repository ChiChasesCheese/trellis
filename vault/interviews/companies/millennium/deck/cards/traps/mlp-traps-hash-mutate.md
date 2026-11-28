---
id: mlp-traps-hash-mutate
node: traps.hash-keys
type: qa
step: 1
---
## Q
**放进 HashSet 后改字段**｜语言陷阱与读代码

类 `P` 有一个 `int id`，`equals` 和 `hashCode` 都按 `id` 实现。输出什么？

```java
Set<P> s = new HashSet<>();
P p = new P(1);
s.add(p);
p.id = 2;
System.out.println(s.contains(p));
System.out.println(s.contains(new P(1)));
System.out.println(s.contains(new P(2)));
System.out.println(s.size());
s.add(p);
System.out.println(s.size());
```

## A
**输出。**
```
false
false
false
1
2
```

- **哈希表按哈希值放桶：** 添加时 `hashCode()` 是 1，元素进了 1 号桶；之后字段改成 2，哈希值变了，对象还留在 1 号桶。
- **`contains(p)` 去 2 号桶找：** 没有，所以 false，尽管对象明明在集合里。
- **`contains(new P(1))` 找到 1 号桶：** 桶里的对象 `id` 已经是 2，`equals` 判不等，所以也是 false。
- **集合里有一个"幽灵"元素：** 删不掉、找不到，`size()` 仍是 1；再 `add(p)` 就多出第二份，size 变 2。
- **记住：** 进入哈希集合或作为 `HashMap` 键的对象，参与 `equals` 和 `hashCode` 的字段必须不可变；用 `final` 字段或 `record`。

**英文答法。**
- "The object stays in its **old bucket**, but lookups now go to the **new hash's** bucket."
- "Keys must be **immutable**; I'd make the fields `final` or use a record."
