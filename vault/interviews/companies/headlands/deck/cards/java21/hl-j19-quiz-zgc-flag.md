---
id: hl-j19-quiz-zgc-flag
node: java21.j19-runtime-zgc-jit
type: qa
step: 41
---
## Q
为什么 JDK 21 里只写 `-XX:+UseZGC` 可能不是你想要的？

## A
JDK 21 里 `-XX:+UseZGC` 默认是**非分代的旧 ZGC**（`ZGenerational` 默认 `false`）。要分代必须再加 `-XX:+ZGenerational`，即 `-XX:+UseZGC -XX:+ZGenerational`。JDK 23 起才默认分代。
