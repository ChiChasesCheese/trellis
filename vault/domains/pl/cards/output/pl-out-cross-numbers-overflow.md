---
id: pl-out-cross-numbers-overflow
node: output.cross-numbers
type: qa
step: 2
---
## Q
**32 位整数溢出**｜读代码说输出

**Python**
```python
x = 2**31 - 1
print(x + 1)
```
**Java**
```java
public class Main { public static void main(String[] a) {
    int x = Integer.MAX_VALUE;
    System.out.println(x + 1);
} }
```
**Go**
```go
func main() {
	var x int32 = 2147483647
	x++
	fmt.Println(x)
}
```
**Rust**
```rust
fn main() {
    let n = std::env::args().count() as i32;
    let x = i32::MAX - 1 + n;
    println!("{}", x + 1);
}
```

输出什么？

## A
**输出。**
**Python**
```
2147483648
```
**Java**
```
-2147483648
```
**Go**
```
-2147483648
```
**Rust**
```
thread 'main' panicked: attempt to add with overflow
```
（debug 构建；用 rustc -O 编译后输出 -2147483648）

**为什么。**
- Python 的 `int` 是任意精度（arbitrary precision），不会溢出，这里用 `2**31 - 1` 模拟 32 位最大值。
- Java 和 Go 的有符号整数按补码回绕，不报错。
- Rust 的 debug 构建检查溢出，直接 panic：`attempt to add with overflow`；用 `-O` 编译的 release 构建默认回绕，得 -2147483648。
- C++ 有符号整数溢出是未定义行为，编译器可以假设它不发生，不能说它打印什么；无符号是定义好的回绕，`UINT_MAX + 1u` 得 0。

**语言为什么这样设计。**
- Java 和 Go 把回绕写进规范，换来可预测、可移植（哈希函数还故意依赖回绕）；C++ 把未定义留给优化器，例如 `x + 1 > x` 可以直接折叠成 true；Rust 折中：debug 里抓 bug，release 里要速度。
- Python 用大整数避免问题，代价是更慢、更占内存。

**怎么写才对。**
```rust
x.checked_add(1)      // 溢出得到 None
x.wrapping_add(1)     // 明确要回绕
x.saturating_add(1)   // 卡在最大值
```
```java
Math.addExact(x, 1)   // 溢出抛 ArithmeticException
```

**面试里一句话。**
Java and Go wrap on overflow, Rust panics in debug and wraps in release, C++ signed overflow is undefined, and Python never overflows.
