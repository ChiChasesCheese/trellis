---
id: errors-bug-vs-failure-user-caused
node: errors.bug-vs-failure
type: qa
step: 2
---
## Q
评论服务的路由是 `/comments/<id>`，请求写成了 `/comments/abc`，代码里直接 `int(path_id)`，用户拿到 500。这是用户的错还是代码的缺陷？

## A
**用户能触发的 500，一定是缺陷**

- **输入由外部决定**：任何调用方能构造出来的值，代码都要给出合同里的回答，不是崩溃；
- **所以这里的 500 是我们漏了校验**：该返回 400（格式错）或 404（不存在），区别要写进合同；
- **同一个 `ValueError` 可能属于两边**：在边界解析外部输入时它是预期失败；在内部算出一个本该是数字的值时它是缺陷，看它出现在哪里；
- **极端输入也算**：空串、几千位的数字串；`int()` 对超过 4300 位的字符串抛 `ValueError`（3.11 起的默认上限），照样是 400；
- **做法**：在边界解析一次，解析失败走失败分支，里面就不再担心格式。

```python
def status(path_id: str) -> int:
    try:
        n = int(path_id)
    except ValueError:
        return 400                       # 调用方能造成的，就是预期失败
    return 200 if n in {1, 2} else 404

print([status(x) for x in ("1", "abc", "9", "", "9" * 5000)])   # [200, 400, 404, 400, 400]
```

**知识点：**缺陷与预期失败（Bugs vs Failures）
