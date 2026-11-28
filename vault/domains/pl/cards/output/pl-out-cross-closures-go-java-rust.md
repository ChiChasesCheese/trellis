---
id: pl-out-cross-closures-go-java-rust
node: output.cross-closures
type: qa
step: 2
---
## Q
**Go、Java、Rust 怎么避开**｜读代码说输出

**Go（同一份代码，go.mod 分别写 go 1.21 和 go 1.22 各运行一次）**
```go
func main() {
	var fs []func() int
	for i := 0; i < 3; i++ {
		fs = append(fs, func() int { return i })
	}
	for _, f := range fs { fmt.Print(f(), " ") }
	fmt.Println()
}
```
**Java**
```java
public class Main { public static void main(String[] x) {
    List<Supplier<Integer>> fs = new ArrayList<>();
    for (int i : new int[]{0, 1, 2}) fs.add(() -> i);
    for (var f : fs) System.out.print(f.get() + " ");
    System.out.println();
} }
```
**Rust**
```rust
fn main() {
    let mut fs: Vec<Box<dyn Fn() -> i32>> = Vec::new();
    for i in 0..3 {
        fs.push(Box::new(move || i));
    }
    for f in &fs { print!("{} ", f()); }
    println!();
}
```

输出什么？

## A
**输出。**
**Go（go 1.21）**
```
3 3 3
```
**Go（go 1.22）**
```
0 1 2
```
**Java**
```
0 1 2
```
**Rust**
```
0 1 2
```

**为什么。**
- Go 1.21 及以前，`for i := 0; …` 的 `i` 整个循环只有一个变量，三个函数共享，结束时 `i = 3`。Go 1.22 起每次迭代有自己的 `i`，由 `go.mod` 里的 `go` 版本行决定。
- Java 的 lambda 只能捕获 effectively final 的局部变量。传统 `for (int i = 0; i < 3; i++)` 里 `i` 会变，编译直接报错 `local variables referenced from a lambda expression must be final or effectively final`；增强 for 每次迭代是新变量，合法，得 0 1 2。
- Rust 的 `move` 把每次的 `i` 拷进闭包；去掉 `move`，编译器报 `` `i` does not live long enough ``，因为借用的 `i` 活不过一次迭代。

**语言为什么这样设计。**
- Go 团队查过大量真实代码，旧语义导致的 bug 远多于依赖它的代码，所以在 1.22 打破兼容，并用 `go.mod` 的版本行让旧项目保持旧行为。
- Java 8 设计 lambda 时选择「值捕获加不可变」：局部变量在栈上，lambda 可能在方法返回后才执行，拷贝值只有在变量不再变化时才不令人意外。

**怎么写才对。**
```go
for i := 0; i < 3; i++ {
    i := i                       // 旧版本 Go 的写法：每次迭代重新声明
    fs = append(fs, func() int { return i })
}
```

**面试里一句话。**
Go 1.22 gives each loop iteration its own variable, Java refuses to capture a changing local, and Rust makes you move the value in.
