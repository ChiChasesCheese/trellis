---
id: hl-cq-q25-errors-narrow-typename-link
node: cpp-questions.f-ub-debug
type: qa
step: 13
---
## Q
三个常见编译 / 链接错误怎么认、怎么修：（1）`non-constant-expression cannot be narrowed from type 'long' to 'int' in initializer list`；（2）`missing 'typename' prior to dependent type name 'C::value_type'`；（3）`Undefined symbols … "square(int)", referenced from: _main`。

## A
- **窄化转换**：花括号初始化禁止窄化（`int x{big}`、`vector<int>{1, 2.5}`）；用 `static_cast<int>(...)` 明确写出，或改类型。
- **缺 `typename`**：模板里依赖名字要标明是类型；写 `typename C::value_type x = …`。
- **未定义符号**（链接错误）：声明了没定义，或没链接那个 `.cpp`；补定义，或把文件加进编译命令。
