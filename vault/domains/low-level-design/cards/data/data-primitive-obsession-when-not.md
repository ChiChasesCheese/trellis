---
id: data-primitive-obsession-when-not
node: data.primitive-obsession
type: qa
step: 4
---
## Q
有同事想给用户名、邮箱、城市、标题都建一个包装类。什么时候包装一个原始值是值得的，什么时候是过度设计？

## A
**包装带来规则或者混淆风险时才值得**

- **值得**：有校验规则（金额必须是正整数）；有操作（`Money.plus` 保证币种一致）；容易互换（两个 id 都是 `int`）；格式藏在字符串里要反复切分；
- **不值得**：只做搬运、没有规则的字段；只在一个函数里出现的局部变量；
- **返回多个值时**：多于两个就用 `NamedTuple` 或 dataclass 取代 `tuple`，不再靠下标取值；
- **只是想让参数不被填反**：`*` 后面强制写名字，不用建新类（见代码）；
- **包装的成本**：多一个类、转换代码、序列化时要拆开；每个类必须物有所值，评审时问“它保护了哪条规则”。

```python
def transfer(*, src: int, dst: int, amount: int) -> str:     # 不建新类，只强制写名字
    return f"move {amount} from {src} to {dst}"

print(transfer(src=7, dst=9, amount=500))
try: transfer(500, 7, 9)
except TypeError as e: print("rejected:", e)
```

**知识点：**用小类型代替裸值（Primitive Obsession）
