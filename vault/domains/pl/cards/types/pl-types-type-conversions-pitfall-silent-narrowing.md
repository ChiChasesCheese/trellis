---
id: pl-types-type-conversions-pitfall-silent-narrowing
node: types.type-conversions
type: qa
step: 6
---
## Q
数值强制转换在 Java 和 Go 里悄悄出错的典型例子是什么？向下转型失败时又是什么现象？

## A
Java 的强制转换从不检查范围：

```java
System.out.println((byte) 200      // -56
    + " " + (int) 3.99             // 3，向零截断，不是四舍五入
    + " " + (int) Double.NaN       // 0
    + " " + (int) 1e20);           // 2147483647，饱和
```

实际输出 `-56 3 0 2147483647`。四个都没有任何警告或异常。

Go 同样：

```go
var x int32 = 300
fmt.Println(uint8(x))   // 44
f := 3.99
fmt.Println(int(f))     // 3
```

实际输出 `44` 和 `3`。注意只有变量转换才会静默截断；对常量，Go 在编译期就拒绝（`cannot convert ... (untyped float constant 3.99) to type int32`）。

生产里的典型后果：把 `long` 的时间戳、ID 或文件大小强制转成 `int`，在小数据下一切正常，超过 21 亿以后变成负数，排序、分页、分配缓冲区全部出错，且没有任何异常；浮点转整数时误以为是四舍五入，金额少了一分。

向下转型失败的现象则是响亮的：

```console
java.lang.ClassCastException: class java.lang.String cannot be cast to class java.lang.Integer
panic: interface conversion: interface {} is string, not int
```

这两种至少会停下来。静默的数值缩窄比响亮的转型失败更危险，因为错误数据会一路流到存储里。对策：缩窄用检查型 API（`Math.toIntExact`、`try_from`），浮点转整数先明确取整方式（`Math.round`、`math.Round`）。
