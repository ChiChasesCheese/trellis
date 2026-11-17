---
id: testing-test-first-check-order
node: testing.test-first
type: qa
step: 5
---
## Q
评论接口规定：先校验正文，再校验用户。要为「检查顺序」写测试，为什么只写「正文为空」和「用户不存在」两个测试不够？

## A
**测顺序要让两个输入同时出错**

- **单错的测试看不出顺序**：正文为空、用户存在，只会触发第一条检查；用户不存在、正文正常，只会触发第二条；两种顺序的实现都通过；
- **双错的输入**：正文为空**且**用户不存在，断言得到的是合同里排在前面的那个错误；
- **为什么顺序是合同的一部分**：调用方按错误码决定下一步，顺序变了，同一个请求会得到不同的处理；
- **同样的做法适用于**：任何「先 A 后 B」的规则，如先语法后策略、先校验后改状态；
- **最后**：把顺序写成一条参数化用例，错误码和输入一起列在表里。

```python
USERS = {"ann"}

def post(user: str, text: str) -> str:
    if not text.strip(): raise ValueError("empty_text")      # 合同：先看正文
    if user not in USERS: raise ValueError("unknown_user")
    return "ok"

def code(user: str, text: str) -> str:
    try: return post(user, text)
    except ValueError as e: return str(e)

print(code("ann", ""), code("bob", "hi"))    # empty_text unknown_user：单错看不出顺序
print(code("bob", ""))                        # empty_text：双错才证明正文在前
```

**知识点：**先写失败的测试（Test First）
