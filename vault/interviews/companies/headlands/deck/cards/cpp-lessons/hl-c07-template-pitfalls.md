---
id: hl-c07-template-pitfalls
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 13
---
## Q
C++ 模板、constexpr 有哪六个常见的坑？

## A
1. **模板代码膨胀**：每个类型一份副本，指令缓存压力；公共部分抽成非模板函数。
2. **报错极长**：从最上面的 `error:` 和第一个 `note: candidate` 读起；concepts 能显著缩短。
3. **ODR/头文件**：模板定义要对所有使用它的翻译单元可见。
4. **依赖名需要 `typename`**：如 `typename T::value_type`。
5. **`constexpr` 不等于一定在编译期执行**：只有用在需要常量的上下文（`constexpr` 变量、`static_assert`、数组大小、`consteval`）才强制。
6. 模板里 `auto` 返回类型推导：不同分支类型不一致或推导不到 `void` 会报错。
