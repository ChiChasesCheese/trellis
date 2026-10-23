---
id: hl-j13-ex1-code
node: java21.j13-unnamed-variables
type: qa
step: 10
---
## Q
把下面旧代码改写成 `_` 的新写法：
```java
try { risky(); } catch (IOException e) { retries++; }
for (Order o : orders) { count++; }
list.forEach(x -> n[0]++);
```

## A
```java
try { risky(); } catch (IOException _) { retries++; }
for (Order _ : orders) { count++; }
list.forEach(_ -> n[0]++);
```
三处都是声明了却不引用：catch 参数、增强 for 变量、lambda 参数。新写法让编译器知道「我故意不用」，不再产生未使用警告，读者也不用再扫一遍代码块确认。
