---
id: pl-abstraction-bounds-variance-pitfall-wildcard-write
node: abstraction.bounds-variance
type: qa
step: 10
---
## Q
使用通配符时最常见的错误是什么？`List<?>`、`List<Object>` 和 `List<? extends Number>` 的混淆会引起什么后果？

## A
最常见的混淆：以为 `List<Object>` 是「任何列表」的通用类型。它不是——泛型不变，`List<String>` 不能传给 `List<Object>` 参数，只能传给 `List<?>`。

```java
List<Integer> ints = new ArrayList<>();
List<Number> ns = ints;       // error: List<Integer> cannot be converted to List<Number>
List<? extends Number> ok = ints;   // 可以，但从此只能读
ok.add(3);                    // error: int cannot be converted to CAP#1
```

于是常见的现场是：开发者在写一个工具方法 `printAll(List<Object> xs)`，发现传不进 `List<String>`，随手改成 `List<?>`，又发现不能往里加元素；再随手加一个强转或 `@SuppressWarnings`，绕过去了，类型安全随之消失。

三种写法的真实含义：

- `List<Object>`：元素类型恰好是 `Object`，可读可写任何对象，但只接受这一种列表。
- `List<?>`：元素类型未知，只能读（得到 `Object`），不能写（`null` 除外）；接受任何列表。
- `List<? extends Number>`：元素是某种未知的 `Number` 子类，只能读（得到 `Number`）。

判断步骤：先问「这个方法对列表做什么」。只读：用 `? extends`；只写：用 `? super`；既读又写：用泛型方法 `<T> void f(List<T> xs)`，让 `T` 把读写联系起来（交换元素这类场景尤其需要）。
