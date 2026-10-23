---
id: hl-j16-varhandle-code
node: java21.j16-concurrency-primitives
type: qa
step: 17
---
## Q
写出声明并使用字段 `ready`（`int`）的 `VarHandle` 的完整代码，并说明三个要点：`static final`、强转、另外两种工厂。

## A
```java
private static final VarHandle READY;                 // 一定要 static final！
static {
    READY = MethodHandles.lookup().findVarHandle(Box.class, "ready", int.class);
}
READY.setRelease(this, 1);
int v = (int) READY.getAcquire(this);                 // 多态签名，返回 Object，要强转
READY.compareAndSet(this, 0, 1);
```
- 访问方法是**签名多态**的（`Object... args`，编译器按实际参数类型生成调用），返回值需手动 cast；错误类型在运行时才抛 `WrongMethodTypeException`/`ClassCastException`。
- 另外两种工厂：`MethodHandles.arrayElementVarHandle(long[].class)`（数组元素）、`MethodHandles.byteArrayViewVarHandle(long[].class, ByteOrder.BIG_ENDIAN)`（把 `byte[]` 当 `long` 序列读）。
