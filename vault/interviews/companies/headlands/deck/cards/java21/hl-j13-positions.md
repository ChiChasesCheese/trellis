---
id: hl-j13-positions
node: java21.j13-unnamed-variables
type: qa
step: 4
---
## Q
未命名变量（unnamed variable）`_` 可以出现在哪六个声明位置？各写一个例子。

## A
```java
catch (NumberFormatException _) { return -1; }     // catch 参数
for (String _ : names) n++;                        // 增强 for 变量
var _ = map.put("k", 1);                           // 局部变量，必须有初始化
try (var _ = new Res()) { ... }                    // try-with-resources
computeIfAbsent("z", _ -> 0);  (_, _) -> 42       // lambda 参数
for (int i = 0, _ = sideEffect(); i < n; i++)      // 传统 for 的初始化
```
`var _ = map.put(..)` 明示「我故意丢弃返回值」。`try (var _ = new Res())` 只要资源「打开→自动关闭」的生命周期（锁、计时器、测试 fixture），不调用它的方法。
