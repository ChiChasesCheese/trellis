---
id: hl-j12-flaw-mutable
node: java21.j12-scoped-values
type: qa
step: 4
---
## Q
`ThreadLocal` 的第三个结构性毛病：可变，随处可改。具体有什么后果？

## A
拿到 `ThreadLocal` 引用的代码都能 `set`，读代码的人答不出「这个值是谁在什么时候改的」。实验里子代码把主线程的 `USER` 改成了 `mallory`，别的代码毫不知情。

要临时改值再还原，只能手写：

```java
var old = USER.get();
try { USER.set(x); ... } finally { USER.set(old); }
```
漏掉任何一步都会污染后续代码。`ScopedValue` 的设计目标就是同时消灭这三个毛病：生命周期失控、不跨线程/继承成本高、可变。
