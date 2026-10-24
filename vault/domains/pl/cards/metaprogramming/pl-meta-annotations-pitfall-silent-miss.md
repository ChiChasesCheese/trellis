---
id: pl-meta-annotations-pitfall-silent-miss
node: metaprogramming.annotations-decorators
type: qa
step: 10
---
## Q
Java 注解的保留策略（retention）和 Go struct tag 的格式错误，为什么会「悄悄失效」？真实表现是什么？

## A
两者的共同点：标记错了，编译器不报错，运行时也不抛异常，只是行为不对。

**Java**：注解默认的保留策略是 `CLASS`，运行时反射看不到它。

```java
@interface Plain {}
@Retention(RetentionPolicy.RUNTIME) @interface Kept {}
@Plain @Kept static class A {}
// A.class.isAnnotationPresent(Plain.class) -> false
// A.class.isAnnotationPresent(Kept.class)  -> true
```

真实输出：`Plain visible: false`，`Kept visible:  true`。自己写的注解忘了 `@Retention(RUNTIME)`，框架读不到，表现为「注解完全没生效」，没有任何报错。

**Go**：tag 的格式是 `key:"value"`，冒号后多一个空格就整个失效。

```go
Email string `json: "email"`   // space after the colon
// output: {"name":"a","Email":"a@x.com"}   (key not renamed)
// go vet: struct field tag `json: "email"` not compatible with
//         reflect.StructTag.Get: bad syntax for struct tag value
```

字段没有被改名，JSON 里仍是 `Email`，没有任何运行时报错，只有 `go vet` 能抓到。

**防线**：Java 为自定义注解写一个测试，断言反射能读到；Go 在 CI 里必须跑 `go vet`。原则是：靠约定工作的标记，必须有一道工具来验证约定。
