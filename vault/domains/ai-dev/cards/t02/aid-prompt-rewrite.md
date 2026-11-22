---
id: aid-prompt-rewrite
node: t02.prompt-scope-constraints-references
type: qa
step: 2
tags: [考点]
---
## Q
**Prompt · 改写练习**｜考点 · 必会

把"加一个日历组件"改成一条能让 agent 一次做对的 prompt。

## A
**改写：**

```text
follow the pattern in HotDogWidget.php and build a calendar widget
that lets you pick a month and page between years. no new libraries.
```

| 改了什么 | 对应要素 |
|---|---|
| 指向现有实现 HotDogWidget.php | references |
| 说明交互：选月份、翻年份 | scope |
| no new libraries | constraints |

**还缺的一项：** done criterion。更好的版本再加一句"组件有测试，跑 `pnpm test widgets` 通过"。

**别这么写：** "做一个好看的、可复用的、灵活的日历组件"——形容词没有判据，agent 会按自己的理解补全，通常是最保守或最花哨的一个。

**出处：** Claude Code docs《Best practices》（Write a specific prompt）
