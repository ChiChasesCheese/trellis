---
id: pl-abstraction-generics-pitfall-java-heap-pollution
node: abstraction.generics
type: qa
step: 10
---
## Q
Java 的泛型安全保证在什么情况下会失效？堆污染（heap pollution）怎么在远离出错点的地方才爆发？

## A
泛型的检查只在编译期，运行期集合里存的就是 `Object`。只要有一处绕过编译器（原始类型、不受检转换、反射），错误的元素就能放进 `List<String>`，而异常要到**读出来的那一刻**才抛。

```java
List<String> names = new ArrayList<>();
List raw = names;                 // 原始类型，只有 unchecked 警告
raw.add(42);                      // 编译通过，运行也不报错
System.out.println(names.size()); // 1
String s = names.get(0);          // 在这里抛 ClassCastException:
// Integer cannot be cast to String
```

污染发生在 `raw.add(42)`，异常却出现在 `get(0)` 之后，二者可能隔着很多层调用、甚至不同线程。堆栈只指向读取处，真正的错误来源没有留下痕迹。

常见入口：老代码或第三方库返回原始类型；`@SuppressWarnings("unchecked")` 压掉了本该看的警告；JSON 反序列化把 `Map<String, Object>` 强转为 `Map<String, String>`。

防御：编译参数打开 `-Xlint:unchecked` 并把警告当错误；每个 `@SuppressWarnings("unchecked")` 都写明为什么安全，范围缩到最小；在系统边界（反序列化、反射）处用 `Class<T>.cast()` 或显式校验，让错误在进入处就暴露。对比 Rust 和 Go：它们没有原始类型这个后门，泛型的保证在运行期同样成立。
