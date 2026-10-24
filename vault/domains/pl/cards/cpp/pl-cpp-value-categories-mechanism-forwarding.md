---
id: pl-cpp-value-categories-mechanism-forwarding
node: cpp.value-categories
type: qa
step: 6
---
## Q
完美转发（perfect forwarding）解决什么问题？转发引用（forwarding reference）和 `std::forward` 是怎样工作的？

## A
**问题**：写一个包装函数（如 `emplace_back`、`make_unique`）时，要把参数原样交给内部函数——调用者传左值，内部收到左值；传右值，内部收到右值。如果为每种组合手写重载，参数 n 个就要 2^n 个。

**转发引用**：在模板里 `template <class T> void f(T&& x)`，这里的 `T&&` **不是**右值引用，而是能绑定任何东西的转发引用。推导规则：传左值时 `T` 被推成 `string&`，传右值时 `T` 被推成 `string`。再靠**引用折叠**：`string& &&` 折叠成 `string&`，`string &&` 保持为 `string&&`。于是 `x` 的类型总是与调用者传入的值类别一致。

**但 `x` 作为表达式仍是左值**（有名字），所以需要 `std::forward<T>(x)`：当 `T` 是左值引用类型时返回左值，否则转成右值。它是一个**有条件的 `std::move`**。

**实测**（`sink` 有 `const string&` 与 `string&&` 两个重载）：

```cpp
template <class T> void bad_wrap(T&& x)  { sink(x); }
template <class T> void good_wrap(T&& x) { sink(std::forward<T>(x)); }
```

结果：`bad_wrap(string("tmp"))` 走 copy 重载；`good_wrap(string("tmp"))` 走 move 重载；`good_wrap(s)`（`s` 是左值）走 copy 重载。`is_lvalue_reference_v<T>` 在传左值时为 `true`，传右值时为 `false`。

**成本与限制**：转发是纯编译期的类型操作，没有运行时开销；但每种参数组合会生成一份模板实例，且大括号初始化列表、重载函数名等不能被推导，转发失败。

**要记住的一点**：只有在**模板里写 `T&&`**，并且要把参数原样传下去时，才用 `std::forward`；其他情况（普通函数的 `Type&&`）用 `std::move`。
