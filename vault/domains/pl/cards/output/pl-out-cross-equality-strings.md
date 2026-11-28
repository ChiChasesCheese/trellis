---
id: pl-out-cross-equality-strings
node: output.cross-equality
type: qa
step: 2
---
## Q
**字符串怎么比**｜读代码说输出

**Java**
```java
public class Main { public static void main(String[] x) {
    String a = "hi", b = new String("hi");
    System.out.println(a == b);
    System.out.println(a.equals(b));
} }
```
**Python**
```python
a = "hi"
b = "".join(["h", "i"])
print(a is b, a == b)
```
**Go**
```go
func main() {
	a := "hi"
	b := strings.Join([]string{"h", "i"}, "")
	fmt.Println(a == b)
}
```
**C++**
```cpp
int main() {
    const char* a = "hi";
    char b[] = "hi";
    cout << (a == b) << " " << (string(a) == string(b)) << endl;
}
```

输出什么？

## A
**输出。**
**Java**
```
false
true
```
**Python**
```
False True
```
**Go**
```
true
```
**C++**
```
0 1
```

**为什么。**
- Java 的 `==` 比引用，`new String("hi")` 必然是新对象，false；`equals` 比内容，true。
- Python 的 `is` 比身份，`==` 比值；运行时拼出来的字符串是新对象，`a is b` 为 False（CPython 的驻留细节属于实现，不要依赖）。
- Go 的 string 是值类型，`==` 直接比内容，true。
- C++ 的 `const char*` 是指针，`a == b` 比的是地址，两块不同内存，0；包成 `std::string` 才比内容，1。

**语言为什么这样设计。**
- 在「对象即引用」的语言里，`==` 默认比身份最便宜（一次指针比较），比内容要遍历整个字符串。Java 让 `==` 保持这个简单含义，不支持运算符重载，值比较留给 `equals`；Python 用 `__eq__` 让 `==` 可以重载成值比较，同时留着 `is` 比身份。
- Go 和 C++ 的字符串类型是值语义，`==` 就是比内容；C 风格字符串是遗留。

**怎么写才对。**
```java
Objects.equals(a, b)        // Java：null 安全的内容比较
```
```python
a == b                      # Python：值比较；is 只用于 None
```

**面试里一句话。**
Java's == and Python's is compare identity, so compare strings with equals in Java and == in Python.
