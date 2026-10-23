---
id: hl-j04-match-exception-accessor
node: java21.j04-record-patterns
type: qa
step: 15
---
## Q
record 的访问器在模式匹配过程中抛异常，调用方会看到什么异常？为什么这样设计？

## A
所有访问器调用被 `catch (Throwable)` 包住，任何异常被包成 **`MatchException`**，原异常放在 `cause`：

```java
record Bad(int x) { public int x() { throw new IllegalStateException("accessor failed"); } }
switch (o) { case Bad(var x) -> ... }
// MatchException, cause = java.lang.IllegalStateException: accessor failed
```
原因：模式匹配是语言构造，匹配过程中出错应有**统一的异常类型**，而不是让调用方看到一个看似与 `switch` 无关的 `IllegalStateException`。
