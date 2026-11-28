---
id: bagu-loop-react-planning-5-write-react
node: a.agent.loop-react-planning
type: qa
step: 5
---
## Q
**手写 ReAct · 伪代码和每一步的作用**｜必会

面试官：「请手写一个 ReAct 循环，并讲清每一步在防什么。」

## A
**基本回答。** 骨架是一个有步数上限的循环。每轮让模型输出结构化决策：要么 `final` 结束，要么 `tool` 调用。工具名要过白名单，结果写回观察供下一轮使用；同时用一个集合记住已经调过的「工具加参数」，同样的调用再出现就判定无进展，循环跑满仍没结束就返回 `max_steps`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="24" y="4" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="22.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">模型给结构化决策</text>
<rect x="24" y="52" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">是 final 吗？</text>
<rect x="24" y="100" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">同工具同参数见过？</text>
<rect x="24" y="148" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="99.0" y="166.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">工具在白名单里？</text>
<rect x="24" y="196" width="150" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="99.0" y="214.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行并追加观察 obs</text>
<line x1="99" y1="32" x2="99.0" y2="46.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,52.0 96.0,46.0 102.0,46.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="99" y1="80" x2="99.0" y2="94.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,100.0 96.0,94.0 102.0,94.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="99" y1="128" x2="99.0" y2="142.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,148.0 96.0,142.0 102.0,142.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="99" y1="176" x2="99.0" y2="190.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="99.0,196.0 96.0,190.0 102.0,190.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="110" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="110" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="110" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<rect x="206" y="52" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">final → 返回答案</text>
<rect x="206" y="100" width="130" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="118.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">stuck → 退出</text>
<rect x="206" y="140" width="130" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="271.0" y="158.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">unknown_tool</text>
<text x="271.0" y="173.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">当观察，继续</text>
<line x1="174" y1="66" x2="200.0" y2="66.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,66.0 200.0,69.0 200.0,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="190" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<line x1="174" y1="114" x2="200.0" y2="114.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,114.0 200.0,117.0 200.0,111.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="190" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<line x1="174" y1="162" x2="200.0" y2="162.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,162.0 200.0,165.0 200.0,159.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="190" y="157" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<line x1="24" y1="210" x2="10" y2="210" stroke-width="1.2" stroke="currentColor"/>
<line x1="10" y1="210" x2="10" y2="18" stroke-width="1.2" stroke="currentColor"/>
<line x1="10" y1="18" x2="18.0" y2="18.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="24.0,18.0 18.0,21.0 18.0,15.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="248" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没等到 final 就跑满 max_steps → 返回 max_steps</text>
</svg>
一轮里从上到下过四关：是不是结束、是不是重复、工具是否存在，都通过了才真正执行；最左边的回路表示执行完再进下一轮。
**代码。** 完整骨架（注释标出每一行在防什么）：
```python
def run(task, model, tools, max_steps=5):
    seen, obs = set(), []
    for step in range(1, max_steps + 1):
        a = model(task, obs)                    # 结构化决策：final 或 tool
        if a["type"] == "final":
            return {"status": "done", "answer": a["answer"]}
        key = (a["tool"], tuple(sorted(a["args"].items())))
        if key in seen:                         # 同工具同参数再来一次 = 无进展
            return {"status": "stuck"}
        seen.add(key)
        if a["tool"] not in tools:              # 白名单；错误也作为观察返回
            obs.append({"ok": False, "error": "unknown_tool"}); continue
        try:
            obs.append(tools[a["tool"]](**a["args"]))   # 观察写回，下一轮可见
        except Exception as e:                  # 工具出错也当观察，不让循环崩
            obs.append({"ok": False, "error": str(e)})
    return {"status": "max_steps"}
```
**容易错。**
- **工具错误直接抛异常：**整个循环崩掉；工具出错或工具名不存在都要当观察返回，模型读到原因才能改参数或换工具，Trace 里也能看到失败。
- **只有 max_steps 没有 seen：**在跑满步数之前，会一直重复同一个无效调用，白烧 Token。
- **白名单只写在提示词里：**提示词不是安全边界，要在执行前用代码检查，参数也要按 Schema 校验；生产版再加写操作二次确认、每步 Trace、观察截断。
- **seen 的 key 不排序参数：**同样的参数换个顺序就认不出来，所以代码里对参数排了序。

**业务场景。** 模型编造了不存在的工具 `refund_all`：白名单拦下，返回 `unknown_tool` 作为观察，模型下一轮改调 `query_order`。
