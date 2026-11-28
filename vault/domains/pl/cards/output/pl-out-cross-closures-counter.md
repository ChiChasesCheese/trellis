---
id: pl-out-cross-closures-counter
node: output.cross-closures
type: qa
step: 4
---
## Q
**闭包里改外层变量**｜读代码说输出

**Python**
```python
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
a, b = counter(), counter()
print(a(), a(), b())
```
**Python（去掉 nonlocal n）**
```python
def counter():
    n = 0
    def inc():
        n += 1
        return n
    return inc
print(counter()())
```
**Go**
```go
func counter() func() int {
	n := 0
	return func() int { n++; return n }
}
func main() {
	a, b := counter(), counter()
	fmt.Println(a(), a(), b())
}
```
**Java**
```java
public class Main {
    static Supplier<Integer> counter() {
        int[] n = {0};
        return () -> ++n[0];
    }
    public static void main(String[] x) {
        var a = counter(); var b = counter();
        System.out.println(a.get() + " " + a.get() + " " + b.get());
    }
}
```

输出什么？

## A
**输出。**
**Python**
```
1 2 1
```
**Python（去掉 nonlocal n）**
```
UnboundLocalError: cannot access local variable 'n' where it is not associated with a value
```
**Go**
```
1 2 1
```
**Java**
```
1 2 1
```

**为什么。**
- 每次调用 `counter()` 都创建一个新的局部变量 `n` 和一个闭包；`a` 与 `b` 各有自己的 `n`，所以输出 1 2 1。
- Python 里 `n += 1` 是赋值，会把 `n` 当成 `inc` 自己的局部变量，读取时还没有值，抛 `UnboundLocalError: cannot access local variable 'n' where it is not associated with a value`；加 `nonlocal n` 才指向外层的 `n`。
- Go 的闭包直接修改外层变量，该变量因为被引用而逃逸到堆上，不需要特殊语法。Java 不允许修改捕获的局部变量（`int n = 0; return () -> ++n;` 编译报错 effectively final），要借助单元素数组或 `AtomicInteger` 这样的可变容器。

**语言为什么这样设计。**
- Python 没有变量声明语法，赋值即定义局部变量，所以需要 `nonlocal`（PEP 3104，Python 3.0 加入）消除歧义。
- Java 的 lambda 捕获的是值的拷贝，修改拷贝没有意义，语言干脆禁止，逼你显式写出共享的容器；Go 和 JavaScript 捕获变量本身，没有这个限制。

**怎么写才对。**
```java
AtomicInteger n = new AtomicInteger();
return n::incrementAndGet;
```

**面试里一句话。**
Each call to the factory makes a fresh captured variable; Python needs nonlocal to rebind it and Java needs a mutable holder.
