---
id: hl-j12-bind-read-code
node: java21.j12-scoped-values
type: qa
step: 6
---
## Q
写出 `ScopedValue` 声明一个 `USER`、绑定为 `"alice"`、在深层方法里读取的最小代码，并说明绑定何时失效。

## A
```java
static final ScopedValue<String> USER = ScopedValue.newInstance();  // 钥匙，static final

ScopedValue.where(USER, "alice").run(() -> {
    System.out.println(USER.get());   // alice
    deep();                           // deep() 里也能 USER.get()，不需要参数
});                                   // lambda 一结束，绑定自动消失
```
- `ScopedValue<T>` 只是**钥匙**，不装值；值只存在于「绑定」里。
- 绑定只在这个 lambda 执行期间有效，不需要 `try/finally`，块外自动回到未绑定。
