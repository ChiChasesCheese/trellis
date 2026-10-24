---
id: pl-types-strong-weak-unique-python-strong-dynamic
node: types.strong-weak
type: qa
step: 6
---
## Q
Python 是动态类型，为什么仍然被叫做强类型？拿它和 JavaScript 对比，同样的 `"1" + 1` 各得到什么？

## A
强弱看的是隐式转换，和检查时机无关。Python 的运行时类型检查很严格：

```python
"1" + 1     # TypeError: can only concatenate str (not "int") to str
```

JavaScript 同样是动态类型，但会强制转换（coercion）。在 Node 里实际运行：

```javascript
"1" + 1       // "11"，数字被转成字符串
"3" * "4"     // 12，字符串被转成数字
[] + {}       // "[object Object]"
1 + null      // 1，null 被当成 0
```

四行的结果都不报错。结果取决于运算符的转换规则，需要记一张很长的表才能预测。

对比的结论：Python 的动态是「晚检查」，但检查时很严；JavaScript 的动态加弱类型，既晚检查又宽松，所以许多错误既不会在编译期出现，也不会在运行期报错，直接变成错误结果。这解释了为什么 TypeScript 要在 JavaScript 上加静态检查。

在 Python 里写错类型的好处是：错误会在出事的那一行立即抛出，而不是产生一个奇怪的值再传播。动态不等于弱，别把两者混为一谈。
