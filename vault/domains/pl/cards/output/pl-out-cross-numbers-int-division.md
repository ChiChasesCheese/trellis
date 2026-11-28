---
id: pl-out-cross-numbers-int-division
node: output.cross-numbers
type: qa
step: 3
---
## Q
**7 除以 2**｜读代码说输出

**Python**
```python
a, b = 7, 2
print(a / b, a // b)
```
**JavaScript**
```javascript
const a = 7, b = 2;
console.log(a / b, Math.floor(a / b));
```
**Java**
```java
public class Main { public static void main(String[] x) {
    int a = 7, b = 2;
    System.out.println(a / b + " " + (double) a / b + " " + (double) (a / b));
} }
```
**Go**
```go
func main() {
	a, b := 7, 2
	fmt.Println(a/b, float64(a)/float64(b))
}
```

输出什么？

## A
**输出。**
**Python**
```
3.5 3
```
**JavaScript**
```
3.5 3
```
**Java**
```
3 3.5 3.0
```
**Go**
```
3 3.5
```

**为什么。**
- Python 3 的 `/` 永远是真除法（true division），得浮点数 3.5；整除要用 `//`。
- JavaScript 只有一种数值类型 number（IEEE 双精度浮点），`7 / 2` 就是 3.5，取整要用 `Math.floor` 或 `Math.trunc`。
- Java 和 Go 里两个整数相除就是整数除法，得 3。要小数必须先把一个操作数转成浮点；`(double) (a / b)` 先除再转，小数已经丢了，得 3.0，括号的位置决定结果。

**语言为什么这样设计。**
- C 家族里运算符的行为由操作数类型决定，整数除法有余数，和 `%` 配对。Go 还不做隐式数值转换，必须写 `float64(a)`。
- Python 2 里 `7 / 2` 也是 3，常常出 bug；PEP 238 在 Python 3 把 `/` 改成真除法，另加 `//` 做整除，是少见的为了正确性打破兼容的改动。

**怎么写才对。**
```java
double r = (double) a / b;      // 先转再除
```
```go
float64(a) / float64(b)
```

**面试里一句话。**
In C-family languages dividing two integers truncates, so convert one operand to floating point first; Python 3 and JavaScript divide as floats.
