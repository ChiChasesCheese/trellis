---
id: pl-trends-others-intro-typescript
node: trends.other-languages
type: qa
step: 5
---
## Q
TypeScript 的渐进类型（gradual typing）和结构化类型（structural typing）是什么？“类型被擦除”意味着什么，对 Python 的类型注解有什么启示？

## A
**是什么**：TypeScript（微软，2012）是 JavaScript 的超集：任何合法的 JavaScript 都是合法的 TypeScript，你可以逐步添加类型。编译器 `tsc` 检查类型，然后把代码编译成纯 JavaScript。

**渐进类型**：类型是可选的、可以逐个文件或逐个函数添加。有一个逃生类型 `any`，使代码不被检查。这让一个巨大的 JavaScript 代码库可以慢慢迁移，不需要停工重写。

**结构化类型**：类型兼容性看**形状**而不是名字。只要对象有需要的字段就满足：

```ts
interface Named { name: string }
function greet(x: Named): string { return "hi " + x.name; }
const o = { name: "ann", age: 3 };
greet(o);          // ok: o has a `name` string
```

这和 Go 的隐式接口思想相近，与 Java 的名义类型（必须声明 `implements`）相反。

**类型擦除**：类型只存在于编译期，运行时 JavaScript 里没有它们。真实验证：文件里有 `let n: number = "oops"`，`tsc --noEmit` 报 `error TS2322: Type 'string' is not assignable to type 'number'`，但 Node 24 直接运行 `.ts` 文件（它只是剥掉类型）仍然输出 `hi ann`，没有任何运行时检查。

**对 Python 的意义**：Python 的类型注解走了同一条路：注解可选、渐进添加、由外部工具（mypy、pyright）检查、运行时忽略。TypeScript 证明了这个模式在大型代码库里是可行的，并且催生了“为动态语言补静态类型”的整套工具与文化（编辑器补全、重构安全）。

**要记住的一点**：渐进类型的承诺是“你可以逐步获得安全”，它的限制是“保证强度取决于你有多彻底地使用，以及边界处的数据是否被校验”（外部 JSON 仍然可能不符合你声明的类型）。
