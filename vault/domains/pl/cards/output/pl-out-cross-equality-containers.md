---
id: pl-out-cross-equality-containers
node: output.cross-equality
type: qa
step: 3
---
## Q
**数组和列表的相等**｜读代码说输出

**Python**
```python
a, b = [1, 2], [1, 2]
print(a == b, a is b)
```
**JavaScript**
```javascript
const a = [1, 2], b = [1, 2];
console.log(a == b, a === b);
```
**Java**
```java
public class Main { public static void main(String[] x) {
    int[] a = {1, 2}, b = {1, 2};
    System.out.println(a == b);
    System.out.println(a.equals(b));
    System.out.println(Arrays.equals(a, b));
} }
```
**Go**
```go
func main() {
	a, b := [2]int{1, 2}, [2]int{1, 2}
	fmt.Println(a == b)
}
```

输出什么？

## A
**输出。**
**Python**
```
True False
```
**JavaScript**
```
false false
```
**Java**
```
false
false
true
```
**Go**
```
true
```

**为什么。**
- Python 的 `list ==` 逐元素比较，`is` 比身份：两个不同的列表，得 True False。
- JavaScript 的 `==` 和 `===` 对对象都比引用，两个数组字面量是两个对象，false false，语言没有内置深比较。
- Java 的数组不重写 `equals`，`a.equals(b)` 等同于 `a == b`，false；`Arrays.equals` 逐元素比较，true。
- Go 的数组是值，元素可比较时 `==` 逐元素比，true；切片、map、函数不能用 `==`，只能和 `nil` 比，改成切片会编译失败：`invalid operation: a == b (slice can only be compared to nil)`。

**语言为什么这样设计。**
- Go 干脆不让你写有歧义的比较：切片是底层数组的视图，「相等」可以指同一视图，也可以指内容相同，规范不替你选，要用 `slices.Equal`（Go 1.21 起）。
- Python 的内置容器自带值相等；Java 21 的 `record` 自动生成 `equals`，数组是历史遗留的例外；JavaScript 没有值语义的复合类型。

**怎么写才对。**
```java
Arrays.equals(a, b)            // 一维数组
Arrays.deepEquals(a, b)        // 多维数组
```
```go
slices.Equal(a, b)
```

**面试里一句话。**
Arrays and lists compare by identity in JavaScript and Java and by content in Python and Go arrays; use Arrays.equals or slices.Equal.
