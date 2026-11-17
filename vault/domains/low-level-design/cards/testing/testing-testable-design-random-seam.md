---
id: testing-testable-design-random-seam
node: testing.testable-design
type: qa
step: 4
---
## Q
短链接服务用随机码当短码，碰到已存在的码就要重新生成。随机码在测试里怎么稳定地触发「撞车重试」这条几乎碰不到的分支？

## A
**随机源做成可替换的钩子，创建一律经过它**

- **随机码本身测不了**：真实的随机码几乎不会撞车，重试分支永远没被执行；
- **钩子**：构造函数接一个生成器可调用对象，默认用 `secrets`；测试传入按顺序吐出预设值的函数，第二个值故意重复第一个；
- **所有创建都走钩子**：如果某个方法直接调 `secrets.token_urlsafe`，那条路径测试就换不掉；
- **重试要有上限**：测试里用「永远返回同一个码」的生成器证明会放弃并报错，而不是死循环；
- **同样的做法**：随机数种子、UUID、临时文件名，都是把「不确定」放在边界。

```python
import secrets

class Shortener:
    def __init__(self, gen=lambda: secrets.token_urlsafe(4)):
        self._gen, self.table = gen, {}
    def create(self, url: str) -> str:
        for _ in range(5):                       # 重试有上限
            code = self._gen()
            if code not in self.table:
                self.table[code] = url
                return code
        raise RuntimeError("no free code")
codes = iter(["aa", "aa", "bb"])
s = Shortener(lambda: next(codes))
print(s.create("u1"), s.create("u2"))            # aa bb：第二次先撞 aa 再取 bb
```

**知识点：**可测的设计（Design for Testability）
