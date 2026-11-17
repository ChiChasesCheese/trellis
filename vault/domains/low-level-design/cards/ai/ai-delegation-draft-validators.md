---
id: ai-delegation-draft-validators
node: ai.delegation
type: qa
step: 2
---
## Q
为什么“校验函数 + 规则表”适合交给智能体起草？你怎么在不信任它的前提下验收？

## A
**输入输出是一张表，验收只要对表**

- **范围小**：一个纯函数，不碰共享状态，不依赖调用顺序；
- **答案可穷举**：合同能写成“输入 → 期望”的表，边界行一行不漏；
- **验收**：表是你写的，它的实现只要对每一行；你不必读懂它的实现；
- **读一眼**：实现里是否用了会越界的写法（`\d`、不带参数的 `strip()`、`isinstance(x, int)`）；
- **仍然自己定**：校验放在哪一层、失败时抛什么。

```python
def ascii_digits(s: str) -> bool:           # 交给智能体起草的部分
    return s.isascii() and s.isdigit()

TABLE = {"4242": True, "": False, "١٢٣": False,   # 你写的表，合同里 ASCII 才算
         "12 3": False, "²": False, "007": True}
print([s for s, want in TABLE.items() if ascii_digits(s) != want])    # []
```

<details class="pt"><summary>延伸</summary>

`"²".isdigit()` 是 `True`（上标数字也算 digit），所以只写 `isdigit()` 不够，要和 `isascii()` 一起用；表里的 `"²"` 一行就是为它设的。

</details>

**知识点：**该交给 AI 还是自己写（When to Delegate）
