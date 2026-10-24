---
id: pl-abstraction-generics-implementation-pitfall-erasure-limits
node: abstraction.generics-implementation
type: qa
step: 9
---
## Q
Java 擦除在实际开发中会引发什么具体的坑？为什么重载、`instanceof` 和泛型数组会出问题？

## A
擦除的后果在三个地方最容易踩到：

1. **重载冲突**：`void g(List<String>)` 与 `void g(List<Integer>)` 擦除后签名都是 `g(List)`，编译报错：

```java
static void g(List<String> l) {}
static void g(List<Integer> l) {}
// error: name clash: g(List<Integer>) and g(List<String>) have the same erasure
```

2. **运行期类型检查**：`o instanceof List<String>` 不合法，只能写 `o instanceof List<?>`，里面的元素类型无从知道。反序列化库（Jackson、Gson）因此需要「类型令牌」（`TypeReference`、`TypeToken`）：匿名子类会把泛型参数保存在类的签名里，绕过擦除。

3. **泛型数组**：`new List<String>[10]` 非法，因为数组在运行期要检查元素类型，而泛型已被擦除，两者的保证会冲突。只能退而用 `List<?>[]` 加强转，或者改用 `List<List<String>>`。

对应到 Rust：因为单态化，这些问题不存在，每个实例都是完整的具体类型；但实例过多会让二进制和编译时间失控。

实践：Java 公共 API 里不要用泛型重载区分行为，要么改方法名，要么改参数类型；需要运行期类型信息就明确传 `Class<T>`；看到 `@SuppressWarnings("unchecked")` 时，要求写出为什么此处是安全的。
