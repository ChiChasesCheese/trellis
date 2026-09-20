---
id: quality-exceptions-vs-results
node: quality.errors
type: qa
step: 3
---
## Q
什么时候该抛异常，什么时候该返回一个 `None`/结果对象，让调用方自己判断成功还是失败？

## A
预期之内、属于业务逻辑正常分支的失败——用户名不存在、余额不足、库存不够——应该用返回值表达，因为这不是"意外",调用方几乎总是要在成功和失败两条路径上分别写代码,把它做成异常反而是在用控制流跳转表达一个本该是普通分支的判断。真正意外的、破坏了前置条件或代表编程错误的情况——不可能出现的状态、违反了调用契约——应该用异常，因为调用方大概率没有为它写处理逻辑，异常能保证它不会被默默吞掉。

```python
def find_user(user_id: str) -> User | None: ...   # 预期会找不到：返回值
def get_user(user_id: str) -> User:                # 调用方自己发的 id 应该存在：不存在就是数据损坏
    user = find_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user
```
判据不是"这件事有多常见",而是"调用方原本就该为这种情况写代码,还是这种情况本身就意味着某处出了错"。
