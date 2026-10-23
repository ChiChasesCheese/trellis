---
id: hl-j17-jdk21-vs-20
node: java21.j17-ffm-api
type: qa
step: 17
---
## Q
JDK 21 相对 JDK 20，FFM API 的主要变化是什么？

## A
- `Arena` **统一了生命周期管理**；
- 布局路径新增解引用地址布局的元素；
- `Linker` 新增优化短调用的选项；
- 新增基于 libffi 的回退 linker；
- 移除 `VaList`。

JDK 21 是第三次预览，JDK 22 转正。
