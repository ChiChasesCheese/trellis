---
id: pl-out-cross-numbers-divmod
node: output.cross-numbers
type: qa
step: 1
---
## Q
**负数的整除与取模**｜读代码说输出

**Python**
```python
print(-7 // 2, -7 % 2)
```
**Java**
```java
public class Main { public static void main(String[] x) {
    System.out.println(-7 / 2 + " " + -7 % 2);
} }
```
**Go**
```go
func main() {
	a, b := -7, 2
	fmt.Println(a/b, a%b)
}
```
**Rust**
```rust
fn main() {
    let (a, b) = (-7, 2);
    println!("{} {}", a / b, a % b);
}
```

输出什么？

## A
**输出。**
**Python**
```
-4 1
```
**Java**
```
-3 -1
```
**Go**
```
-3 -1
```
**Rust**
```
-3 -1
```

**为什么。**
- Python 的 `//` 向下取整（floor）：-3.5 变成 -4；余数满足 `a == (a//b)*b + a%b`，所以 `-7 % 2` 是 -7 - (-8) = 1，符号跟除数。
- Java、Go、Rust 的 `/` 向零截断：-3.5 变成 -3，余数是 -1，符号跟被除数。C++ 和 JavaScript 的 `%` 同样得 -1。
- Rust 的 `%` 是截断余数（remainder），数学意义的取模要用 `rem_euclid`。

**语言为什么这样设计。**
- 向零截断来自硬件：x86 的除法指令就这样算，C99 才把它写进标准（C89 由实现决定），后来的语言沿用，换来最快的 `/` 和 `%`。
- Python 选 floor，是为了让 `i % n` 永远落在 [0, n)，对环形下标、哈希取模都方便。Rust 同时提供两种：`a / b` 与 `a % b` 截断，`div_euclid` 与 `rem_euclid` 向下取整。

**怎么写才对。**
```java
Math.floorMod(a, b)          // Java
```
```rust
a.rem_euclid(b)              // Rust，-7 与 2 得 1
```
```go
((a % b) + b) % b            // Go、C++、JavaScript
```

**面试里一句话。**
Python floors integer division while Java, Go, Rust, C++ and JavaScript truncate toward zero, so negative remainders differ.
