---
id: hl-cq-q25-compile-error-method
node: cpp-questions.f-ub-debug
type: qa
step: 11
---
## Q
面试题：现场遇到编译错误，怎么快速修？最常见的有哪些？
You get a compile error live in the interview. How do you fix it quickly? What are the most common ones?

## A
- **从第一个错误开始读，修一个就重新编译**——后面的错误经常是连锁反应。
- 先看错误行号和 `note:` 行。
- 记住十来种常见错误的形状。
- 写代码时从一个**能编译的最小 `main`** 起步，小步编译，这样错误总在最后几行。
- 编译时开 `-Wall -Wextra`。
