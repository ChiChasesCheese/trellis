---
id: pl-out-cross-equality-loose
node: output.cross-equality
type: qa
step: 1
---
## Q
**JavaScript 的 == 与 Python**｜读代码说输出

**Python**
```python
print(1 == 1.0, "5" == 5, None == False, [] == False, float("nan") == float("nan"))
```
**JavaScript**
```javascript
console.log(1 == 1.0, "5" == 5, null == false, [] == false, NaN == NaN);
```

输出什么？

## A
**输出。**
**Python**
```
True False False False False
```
**JavaScript**
```
true true false true false
```

**为什么。**
- Python 的 `==` 不转换类型：`1 == 1.0` 是 True 因为数值类型之间定义了相等；字符串与数字、`None` 与 `False`、列表与 `False` 都是 False。
- NaN 与任何值都不相等，包括自己（IEEE 754），两种语言一致。
- JavaScript 的 `==` 是宽松相等（loose equality），类型不同就按抽象相等算法转换：`"5" == 5` 把字符串转成数字；`[] == false` 把 `[]` 转成空串再转成 0，`false` 也是 0，得 true；`null == false` 却是 false，因为 `null` 只等于 `undefined`。

**语言为什么这样设计。**
- JavaScript 早期为方便网页表单里字符串与数字混用，设计了隐式转换，后来用 `===`（严格相等，不转换）补救，`==` 因为兼容无法删除。
- Python、Java、Go 只在同类型或数值族内比较；Rust 连 `1 == 1.0` 都不允许，编译报错 `can't compare `{integer}` with `{float}``。

**怎么写才对。**
```javascript
x === y                    // 永远用严格相等
Number.isNaN(x)            // 判断 NaN
x == null                  // 唯一常见例外：同时匹配 null 和 undefined
```

**面试里一句话。**
JavaScript's == coerces types by a long rule table, so use === and remember NaN is unequal to everything, itself included.
