---
id: pl-out-cross-closures-loop
node: output.cross-closures
type: qa
step: 1
---
## Q
**循环里的闭包**｜读代码说输出

**Python**
```python
fs = []
for i in range(3):
    fs.append(lambda: i)
print(*[f() for f in fs])
```
**JavaScript (var)**
```javascript
const fs = [];
for (var i = 0; i < 3; i++) fs.push(() => i);
console.log(fs.map(f => f()).join(" "));
```
**JavaScript (let)**
```javascript
const fs = [];
for (let i = 0; i < 3; i++) fs.push(() => i);
console.log(fs.map(f => f()).join(" "));
```

输出什么？

## A
**输出。**
**Python**
```
2 2 2
```
**JavaScript (var)**
```
3 3 3
```
**JavaScript (let)**
```
0 1 2
```

**为什么。**
- 闭包（closure）捕获的是变量，不是当时的值。Python 的 `for` 不开新作用域，三个 lambda 共用同一个 `i`，循环结束时 `i = 2`，调用时才读，得到 2。
- JavaScript 的 `var` 是函数作用域，也只有一个 `i`；循环到 `i = 3` 才结束，所以是 3。
- `let` 在 `for` 里每次迭代创建一个新绑定（per-iteration binding），每个箭头函数捕获自己的那份，得 0 1 2。

**语言为什么这样设计。**
- Python 的循环和 if 不开新作用域（作用域边界是函数、类和模块），名字在调用时才查（晚绑定，late binding）。ES2015 的 `let` 就是为修复 `var` 的这个坑而加，`for` 循环还特别规定每次迭代拷贝一份。
- Java 禁止捕获会变化的局部变量，Go 1.22 起每次迭代一个新变量，Rust 要求 `move` 或借用，都在语言层面绕开这个坑。

**怎么写才对。**
```python
fs.append(lambda i=i: i)     # 默认参数在定义时求值
```
```javascript
for (let i = 0; i < 3; i++) …   // 用 let
```

**面试里一句话。**
Closures capture variables, not values, so a loop that reuses one variable gives every closure its final value.
