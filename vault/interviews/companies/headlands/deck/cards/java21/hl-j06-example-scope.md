---
id: hl-j06-example-scope
node: java21.j06-instanceof-pattern
type: qa
step: 13
---
## Q
下面 `or(Object o)` 里，两处 `s` 哪里可用？再写一个用 `while` 配 `instanceof Integer n` 求"遇到非整数就停"的累加。

```java
if (!(o instanceof String s) || s.isEmpty()) {
    return "not a nonempty string";   // (1)
}
return "string " + s;                  // (2)
```

## A
- (1) **不可用**：可能没匹配（`||` 左边为真意味着没匹配）。
- (2) **可用**：能走到这里说明 `||` 两边都为假，即匹配成功且非空。

累加：
```java
int sum = 0, i = 0;
while (i < xs.size() && xs.get(i) instanceof Integer n) { sum += n; i++; }
```
`List.of(1, 2, 3, "stop", 4)` 得 6。
