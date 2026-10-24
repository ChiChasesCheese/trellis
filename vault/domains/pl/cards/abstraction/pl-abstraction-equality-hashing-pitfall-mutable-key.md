---
id: pl-abstraction-equality-hashing-pitfall-mutable-key
node: abstraction.equality-hashing
type: qa
step: 10
---
## Q
在 Java 里把一个可变对象当作 `HashMap` 的键，之后修改它，会发生什么？线上怎么表现？

## A
上一张卡的机制在真实系统里的表现：

```java
static class Key {
    int id; Key(int id) { this.id = id; }
    @Override public boolean equals(Object o) { return o instanceof Key k && k.id == id; }
    @Override public int hashCode() { return id; }
}
Map<Key, String> m = new HashMap<>();
Key k = new Key(1);
m.put(k, "v");
k.id = 2;
System.out.println(m.get(k) + " " + m.get(new Key(1)) + " " + m.size());
// 输出：null null 1
```

用修改后的键查不到，用原来的值也查不到，`size()` 却是 1：条目成了无法访问也无法删除的幽灵。

线上表现为：缓存命中率莫名变低而内存持续上涨（幽灵条目不会被淘汰）；去重集合里出现「重复」元素（同一个逻辑对象在不同哈希下被放进去两次）；在多线程下更难复现。

常见原因：把实体类（带 setter 的 JPA 对象）当键；把 `List<String>` 当键然后继续往里加；用可变的 `StringBuilder` 当键。

防御：
- 键用不可变类型（`String`、`record`、`List.copyOf` 的结果）。
- 实体类的 `equals`/`hashCode` 基于不变的业务 ID，不基于会被修改的字段，也不要基于数据库生成、保存前为 `null` 的主键。
- Rust 和 Python 在语言层给了保护（所有权、不可哈希的可变内置类型）；Java 需要你自己守住这条纪律，代码审查时看到 `Map<某个可变类, ...>` 就应该追问。
