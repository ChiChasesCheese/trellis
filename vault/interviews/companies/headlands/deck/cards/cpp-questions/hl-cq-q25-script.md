---
id: hl-cq-q25-script
node: cpp-questions.f-ub-debug
type: qa
step: 16
---
## Q
用英文 60 秒回答：You get a compile error live in the interview. How do you fix it quickly? What are the most common ones?

## A
结构：从第一个错误读起（连锁错误）→ 熟悉的错误形状（include、const、窄化、no matching function、`typename`、分号、链接错误）→ `-Wall -Wextra` 与最小 `main` 小步加。

- I read from the **first error** - later ones are often cascades; one missing `#include <vector>` produced four errors - fix it, and rebuild.
- I know the usual shapes: missing include or `std::`; **const-correctness** - calling a non-const member on a const reference; **narrowing** in brace initialization; "no matching function" where the `note:` lines show the candidate signatures; a missing `typename` for dependent types in templates; a missing semicolon after a struct; and the **link-time** ones - undefined reference and duplicate symbol.
- I compile with `-Wall -Wextra`, and in a live environment I start from a minimal `main` that builds, then add code in small steps so an error is always in the last few lines.
