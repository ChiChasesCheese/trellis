---
id: pl-types-soundness-pitfall-assertion-boundary
node: types.soundness
type: qa
step: 10
---
## Q
`JSON.parse(...) as Config`（TypeScript）和 `cast(int, json.loads(...))`（Python）为什么会让错误数据一路通过类型检查，在很远的地方才爆发？

## A
类型断言（`as`）和 `cast` 都是对检查器说「我知道这个值是什么类型」。它们**只改变检查器的认知，不检查值本身**，运行时没有任何代码执行。数据来自边界（网络、配置文件），正是最需要检查的地方，断言却把检查整个跳过了。

TypeScript：

```ts
interface Cfg { retries: number }
const cfg = JSON.parse('{"retries": "3"}') as Cfg;
console.log(cfg.retries + 1);       // tsc --strict: no error
console.log(typeof cfg.retries);
```

输出 `31` 和 `string`。类型说 `retries` 是数字，实际是字符串 `"3"`，`+ 1` 变成了字符串拼接，得到 `"31"`，不报错，直接带着错误值流入后续计算（比如重试次数变成了 31 次）。

Python：

```python
from typing import cast
import json
n = cast(int, json.loads('"7"'))
print(n + 1)
```

`mypy` 报告 `Success: no issues found`；运行时抛出 `TypeError: can only concatenate str (not "int") to str`。这里至少抛出了异常，而 TypeScript 的版本悄悄产生了错误结果。

两者的共同点：类型是**声明**出来的，不是**验证**出来的。问题的位置（边界处的断言）和症状的位置（几层调用后的某次运算）相隔很远，没有堆栈能把你带回到那条断言。

对策是让类型成为验证的**结果**：

- TypeScript：用 zod、io-ts 之类的校验库，`schema.parse(data)` 在运行时检查并返回有类型的值；或手写类型守卫函数 `isCfg(x): x is Cfg`，里面做真实的检查。
- Python：用 pydantic 的 `Model.model_validate(data)`，或 `dataclass` 加手写校验，类型由构造过程保证。
- Java 的 Jackson 反序列化到具体类，类型不符时当场抛异常，也是同样的思路；Rust 的 `serde` 反序列化失败返回 `Err`，没有「断言」这条捷径。

规则：**每一个 `as`、`cast` 都是一处潜在的类型漏洞；它们应当出现在经过校验之后，而不是代替校验。**
