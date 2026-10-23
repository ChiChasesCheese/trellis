---
id: hl-cq-q24-compile-flags
node: cpp-questions.f-ub-debug
type: qa
step: 6
---
## Q
写出用 clang++ 同时开 ASan 和 UBSan 的编译命令，以及开 TSan 的命令。TSan 能和 ASan 同时开吗？

## A
```
clang++ -std=c++20 -g -O1 -fno-omit-frame-pointer -fsanitize=address,undefined x.cpp
clang++ -std=c++20 -g -O1 -fno-omit-frame-pointer -fsanitize=thread x.cpp
```
- **TSan 不能和 ASan 同时开**，要分两次构建。
- 测速度时要去掉 sanitizer，用不带 sanitizer 的 `-O2`。
