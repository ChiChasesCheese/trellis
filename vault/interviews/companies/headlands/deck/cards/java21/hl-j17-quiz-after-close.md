---
id: hl-j17-quiz-after-close
node: java21.j17-ffm-api
type: qa
step: 24
---
## Q
下面代码运行会怎样？为什么不会崩进程？
```java
MemorySegment s;
try (var a = Arena.ofConfined()) { s = a.allocate(16, 8); }
s.get(ValueLayout.JAVA_LONG, 0);
```

## A
抛 `IllegalStateException`（`Already closed`），**不崩进程**，因为每次访问都检查生命周期（所属 `Arena` 是否还活着）。这避免了 C 里的 use-after-free 段错误。

注意：`s` 仍持有引用、不是 `null`，是运行时错误而非编译错误；所以不要把 segment 存进比 arena 活得更久的对象。
