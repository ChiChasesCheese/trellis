---
id: hl-j08-bad-uses
node: java21.j08-var
type: qa
step: 20
---
## Q
哪三种情形不适合用 `var`？`var total = 0; total += qty;`（`qty` 是 `long`）为什么危险？

## A
1. **右边是方法调用，看不出返回类型**：`var x = foo.process(input);`，读者得翻 `foo` 的定义。写出类型是对读者的善意。
2. **字面量参与运算**：`var total = 0;` 之后 `total += qty` 能编译（复合赋值隐式窄化），但结果被悄悄截成 `int`。数字类型是业务语义，应显式写 `long total = 0;`。
3. **希望变量类型是接口 / 父类**：`List<Fill> list = new ArrayList<>();`。
