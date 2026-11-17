---
id: refactoring-abs-unwind
node: refactoring.over-abstraction
type: qa
step: 4
---
## Q
团队里有个叫 `send(msg, via, html, retry)` 的函数，里面四个开关互相牵制，每个调用方只用其中一两种组合。想把它拆回去，怎么做才不引入新缺陷？

## A
**先内联回每个调用点，再只留下真正共同的部分**

- **第一步：把函数内联到每个调用方**：每个调用点用到的开关组合是确定的，把不会走到的分支删掉；
- **第二步：看哪些代码是真的重复**：内联后每个调用点都变得很短，共同的几行再提成一个小函数，名字描述它做什么；
- **每一步都靠测试守住**：用调用方实际用到的组合写特征测试，内联前后输出一致；
- **别一次改完**：一个调用点内联、测试、提交，再做下一个；
- **删掉用不到的开关**：没有调用方用到的参数，直接删，不是“以后可能要”。

```python
def send(msg, via, html=False, retry=False):          # 旧：开关牵制
    body = f"<p>{msg}</p>" if html else msg
    out = f"{via}:{body}"
    return out + ("!" if retry else "")

def send_email(msg): return f"email:<p>{msg}</p>"     # 内联后：调用点 1 只用 html
def send_sms(msg): return f"sms:{msg}"                # 内联后：调用点 2 只用普通文本

assert send("hi", "email", html=True) == send_email("hi")
assert send("hi", "sms") == send_sms("hi")            # 行为不变
print(send_email("hi"), send_sms("hi"))
```

**知识点：**过度抽象（Over-Abstraction）
