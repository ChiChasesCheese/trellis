---
id: py-out-identity-string-intern
node: output.identity
type: qa
step: 4
---
## Q
**字符串驻留**｜读代码说输出

```python
import sys
a = "hello world"
b = "".join(["hello", " world"])
print(a == b, a is b)
print(sys.intern(a) is sys.intern(b))
```

输出什么？

## A
**输出。**

```
True False
True
```

**为什么。**

- 内容相同，所以 `a == b` 为 True；`join` 在运行时新建了字符串对象，和字面量不是同一个，`a is b` 为 False。
- `sys.intern` 把字符串放进驻留表（intern table），内容相同的字符串返回表里唯一的那个对象，所以两次 `intern` 的结果是同一个对象。
- CPython 只会自动驻留看起来像标识符的字符串常量，运行时造出来的不在其中。

**语言为什么这样设计。**

- 驻留让标识符、属性名、字典键的比较变成指针比较，速度快；但对所有字符串都查表有成本，所以只自动做一部分，其余交给 `sys.intern`。
- Java 的字符串字面量池和 `String.intern()` 是同一思路，`==` 比较字符串同样是经典坑；语言层面它们都只保证 `equals`。

**怎么写才对。**

```python
a == b                 # 比内容
sys.intern(s)          # 大量重复字符串当键时省内存
```

**面试里一句话。**

String interning is an optimization that Python applies only to some strings, so equality must use == and never is.
