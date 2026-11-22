---
id: tc-code-samples
node: t04.writing-code-samples
type: qa
step: 1
tags: [原则]
---
## Q
**Writing code samples · 示例代码**｜原则 · 追问

你在 README 里放了一段示例代码：十几行初始化，一个 `Level(5, 28, 48)`，一行 "Create a stream from the file." 的注释。读者复制后跑不起来。该怎么改？

## A
**原则：** 示例代码的唯一目标是**教学**。它要正确、简洁、易懂、可复用，并且按从简单到复杂的顺序排列。

**怎么做：**
1. **正确：** 能编译、能跑、输出和文字说的一致；定期测试，因为系统会变。
2. **简洁：** 只放必要的代码，不放无关细节；但别为了短牺牲正确。
3. **易懂：** 用有意义的名字；避免炫技和深层嵌套；参数写名字，如 `Level(rank=5, dimension=28, opacity=48)`。
4. **注释不写显而易见的事：** 解释**为什么**和不明显的参数含义，别重复代码。
5. **可复用：** 写明依赖、环境、怎么运行、预期输出，别有会破坏读者环境的副作用。
6. **严格语法加反例：** 例如 shell 里等号两侧不能有空格，把对的错的都写出来。
7. **按复杂度排序：** 先 hello world，再中等，再复杂。

**常见错法：**
- **把单元测试当示例：** 测试的目标是验证，不是教学。
- **注释只是翻译代码：** "# Create a stream from the file."
- **没有说明预期输出。**

**改写示例：**
```python
# Before
level = go.so.Level(5, 28, 48)
# After: named arguments show what each number means
level = go.so.Level(rank=5, dimension=28, opacity=48)
```

<details class="pt" markdown="1"><summary>出处</summary>

Google Technical Writing Two《Creating sample code》（developers.google.com/tech-writing/two/sample-code）

</details>
