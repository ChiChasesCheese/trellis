---
id: hl-j06-read-long
node: java21.j06-instanceof-pattern
type: qa
step: 16
---
## Q
补全代码：读弱类型配置 `Map<String, Object>` 的值为 `long`：`Integer` 和 `Long` 直接转，非空白 `String` 去空白后解析，否则返回默认值。

## A
```java
static long readLong(Map<String, Object> cfg, String key, long dflt) {
    Object v = cfg.get(key);
    if (v instanceof Integer i) return i;
    if (v instanceof Long l) return l;
    if (v instanceof String s && !s.isBlank()) return Long.parseLong(s.trim());
    return dflt;
}
```
比旧写法的 `((Integer) v).longValue()` 括号套括号干净；`String s && !s.isBlank()` 把类型检查和字段条件合在一个条件里。
