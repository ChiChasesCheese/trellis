---
id: hl-cq-q03-script
node: cpp-questions.a-why-fast
type: qa
step: 19
---
## Q
用英文 60 秒回答：Walk me through what happens between `g++ main.cpp` and a running program. Why do we have header files, and what is the One Definition Rule?

## A
结构：四个阶段 → 翻译单元只见声明、链接器接定义（未定义引用）→ ODR 与 `inline`/模板放头文件 → `<iostream>` 约 8.4 万行解释编译慢与 modules。

- Four stages: **preprocess** - which literally pastes headers in; **compile** - each `.cpp` file separately into an object file; **assemble**; and **link**, which resolves symbols across object files.
- A **translation unit** is one `.cpp` after preprocessing. It only knows the **declarations** it includes; the linker connects calls to definitions. Declared but never defined gives an **undefined reference at link time**.
- The **One Definition Rule**: a non-inline function or variable may be defined once per program - two definitions give a duplicate-symbol link error, which is why header functions are `inline` and templates live in headers.
- Including `<iostream>` expands to about 84 thousand lines, which is why builds are slow and why modules exist.
