---
id: mlp-traps-hash-contract
node: traps.hash-keys
type: qa
step: 2
---
## Q
**只重写 equals，和用 List 当键**｜语言陷阱与读代码

类 `Q` 有 `int id`，只重写了 `equals`（按 `id`），没有重写 `hashCode`。输出什么？

```java
Set<Q> s = new HashSet<>();
s.add(new Q(1));
System.out.println(new Q(1).equals(new Q(1)));
System.out.println(s.contains(new Q(1)));

Map<List<Integer>, String> m = new HashMap<>();
List<Integer> k = new ArrayList<>(List.of(1));
m.put(k, "x");
k.add(2);
System.out.println(m.get(k) + " " + m.get(List.of(1)) + " " + m.get(List.of(1, 2)));
System.out.println(m.size());
```

## A
**输出。**
```
true
false
null null null
1
```

- **`equals` 为 true、`contains` 为 false：** 没重写 `hashCode`，用的是 `Object` 默认的，按对象身份生成，两个 `Q(1)` 几乎一定落在不同的桶里，查找根本没走到 `equals`。
- **约定：** 两个对象 `equals` 为 true，`hashCode` 必须相等；反过来不要求。重写其一必须重写另一个。
- **`List` 当键同样危险：** 放进去时哈希值按 `[1]` 算，后来加了元素，内容变成 `[1, 2]`，哈希值也变。
- **三种查法都找不到：** 用 `k` 查，去新哈希值的桶，空；用 `[1]` 查，找到旧桶，但键现在是 `[1, 2]`，`equals` 不等；用 `[1, 2]` 查，同样去新桶，空。映射里留着一条无法访问的数据，`size` 仍是 1。
- **记住：** `equals` 和 `hashCode` 成对重写，用同一组字段；键用不可变对象（`String`、`Integer`、`record`、`List.copyOf`）。

**英文答法。**
- "If two objects are equal, they must have the **same hashCode**, so I override both."
- "I'd use an **immutable** key, or copy the list before using it as a key."
