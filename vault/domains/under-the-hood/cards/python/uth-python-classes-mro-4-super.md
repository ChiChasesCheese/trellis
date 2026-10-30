---
id: uth-python-classes-mro-4-super
node: python.classes-mro
type: qa
step: 4
---
## Q
**super() 不是「调用父类」**｜Python · CPython 3.14

`M(L, R)` 的 `L`、`R` 都继承 `Base`，并各自在 `__init__` 里调用 `super().__init__()`。创建 `M()` 时，`L` 里的 `super()` 调到的是 `Base` 吗？

## A
**背景。** 菱形里如果 `L` 和 `R` 都直接写 `Base.__init__(self)`，`Base` 会被初始化两次。想要的效果是：每个类只做自己的那一份，然后把球传给「下一个人」，整条链上每个类刚好执行一次。

**结构。** `super()` 的意思是：在 `type(self)` 的 MRO 里找到当前这个类，取它**后面**的那个类。`M` 的 MRO 是 `M L R Base object`，所以 `L` 里的 `super()` 指向 `R`，不是 `Base`。实测创建 `M()` 依次打印 `M`、`L`、`R`、`Base`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="40" y="10" width="90" height="30" rx="3"/>
<rect x="40" y="62" width="90" height="30" rx="3"/>
<rect x="40" y="166" width="90" height="30" rx="3"/>
<line x1="85" y1="40" x2="85" y2="62"/>
<path d="M 130 77 C 215 77 215 181 130 181" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="40" y="114" width="90" height="30" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="85" y1="92" x2="85" y2="114"/>
<line x1="85" y1="144" x2="85" y2="166"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="85.0,62.0 82.0,56.0 88.0,56.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="85.0,114.0 82.0,108.0 88.0,108.0"/>
<polygon points="85.0,166.0 82.0,160.0 88.0,160.0"/>
</g>
<g fill="currentColor">
<text x="85" y="29">M(L, R)</text>
<text x="85" y="81">L</text>
<text x="85" y="133">R</text>
<text x="85" y="185">Base</text>
<text x="222" y="46" text-anchor="start">M L R Base</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="222" y="124" text-anchor="start">不是直接</text>
<text x="222" y="140" text-anchor="start">到 Base</text>
<text x="222" y="30" text-anchor="start">M 的 MRO:</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="95" y="107" text-anchor="start" font-size="11">L 里的 super()</text>
<text x="95" y="159" text-anchor="start" font-size="11">R 里的 super()</text>
</g>
</g>
</svg>
```

**细节。**

- 无参的 `super()` 靠编译器：方法里一旦用了 `super`，编译器就给它加一个隐藏的闭包变量 `__class__`（指向当前类），再取第一个参数 `self`。运行时在 `type(self).__mro__` 里找到 `__class__`，从下一项开始查。
- CPython 3.12 起，`super().method()` 被编译成专用指令 `LOAD_SUPER_ATTR`，不再临时造一个 `super` 对象，更快。

**为什么。** 这叫协作式多继承（cooperative multiple inheritance）：谁都不必知道别人是谁，每个类只管把调用交给 MRO 里的下一个，`Base` 因此只执行一次。

**坑。** 链上只要有一个类忘了调用 `super()`，排在它后面的类就被悄悄跳过。

**对应 LeetCode：** 无直接对应的题
