---
id: pl-types-soundness-foundation-typescript
node: types.soundness
type: qa
step: 3
---
## Q
TypeScript 的类型系统为什么说是「有意不可靠」的？数组协变和方法参数双变分别让哪类错误通过检查？

## A
TypeScript 是 JavaScript 的静态类型层：类型在编译时擦除，生成的 JS 里不再有类型。它的设计目标明确不包括「提供可证明的正确类型系统」，而是在**可靠**与**好用**之间偏向好用，让现有 JS 代码能逐步加类型。结果是有一批有意保留的漏洞。

**数组协变**：`Dog[]` 可以赋给 `Animal[]`（把 `Dog` 看成 `Animal`）。这对只读是对的，对写入就错了：

```ts
const dogs: Dog[] = [new Dog()];
const animals: Animal[] = dogs;     // accepted
animals.push(new Cat());            // accepted, dogs now holds a Cat
console.log(dogs[1].bark());        // accepted by tsc --strict
```

`tsc --strict` 全部通过，运行时抛出 `TypeError: dogs[1].bark is not a function`。

**方法参数双变**：声明为方法（而不是函数属性）的成员，参数类型既可以更宽也可以更窄：

```ts
interface Handler { run(x: Animal): void }
const h: Handler = { run(x: Dog) { x.bark(); } };   // narrower parameter: accepted
h.run(new Animal());   // TypeError: x.bark is not a function
```

本来 `run` 承诺能处理任何 `Animal`，实现却只能处理 `Dog`，按严格规则（参数逆变）应拒绝。TypeScript 放行，因为大量 JS 代码（事件处理器、`Array.prototype` 方法）都依赖这种写法，严格了就很难给已有库加类型。

此外还有：`any`（任意类型、传染性强）、类型断言 `x as T`（只是断言，不是检查）、对象字面量的多余属性、`strictNullChecks` 外的 `null`。

这是一个有意识的工程取舍：宁可放过一些错误，也要让类型层足够宽松，使开发者愿意接受它。代价是 **TypeScript 的类型不是证据**，它是一个有用的提示系统，需要在数据入口（网络、JSON、第三方库）另做运行时校验。
