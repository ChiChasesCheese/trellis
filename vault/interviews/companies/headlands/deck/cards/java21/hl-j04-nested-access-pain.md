---
id: hl-j04-nested-access-pain
node: java21.j04-record-patterns
type: qa
step: 1
---
## Q
Java 8 里取一个嵌套值（如 `Value(Mean(分子, 分母))`）要走哪四步？这种写法有哪三个痛点？

## A
四步：① 判断类型、② 强转、③ 取外层字段、④ 取内层字段（`instanceof Value` → `(Value) a` → `v.getMean()` → `m.getNumerator()`）。

痛点：
1. **"想知道的"被淹没在"怎么取到它"里**：真正的逻辑只有"分母为 1 就打印分子"，却被 6 行取值代码包围。
2. **每层都要手动判断 + 强转 + 调 getter**，嵌套越深越长，强转写错编译器不报。
3. **条件和结构混在一起**：理想是结构用模式写、条件用 `when` 写。
