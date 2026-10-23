---
id: hl-javaq-e-q19-limits
node: java-questions.e-jit-gc
type: qa
step: 7
---
## Q
HotSpot 内联的默认大小阈值（`MaxInlineSize`、`FreqInlineSize`、`MaxInlineLevel`）分别是多少？这对代码设计有什么影响？

## A
- `MaxInlineSize=35`：**冷方法**字节码超过 35 字节不内联。
- `FreqInlineSize=325`：**热方法**的上限。
- `MaxInlineLevel=15`：内联深度。
- 所以**保持热方法小**：400 字节码的巨型方法不会被内联进调用者。
- `final` 方法 / 类、`static`、`private` 方法天然可直接内联（不需要 CHA）。
- 热路径上的接口 / 抽象类若运行时实现类 ≥ 3 种，就要付虚调用代价。
