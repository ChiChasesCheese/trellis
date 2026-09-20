---
id: problems-linkedin-profile-structured-not-dict
node: problems.social.linkedin
type: qa
step: 1
tags: [grown]
---
## Q
在职业社交（LinkedIn）设计里，档案的工作经历、教育经历为什么用 `frozen=True` 的 `dataclass`（如 `ExperienceEntry`）表示，而不是用一个 `dict[str, Any]` 让字段自由扩展？

## A
因为字典的“灵活”是没有强制力的：招聘方按技能搜候选人要假设某个键一定叫 `"name"`，经历排序要假设某个值一定是可比较的日期，这些假设没有任何地方写下来，也没有任何东西阻止拼写不一致或类型错误——出错只会在读取时悄悄发生（搜不到人、排序崩溃），而不是在写入时被类型系统拦下。用结构化的 `dataclass`，字段的类型由定义强制，`start_date` 一定是 `datetime`，“是否在职”（`end_date is None`）这类查询可以直接用；技能作为一个类型明确的字符串，才能被后面的技能反向索引安全引用。真要支持用户自定义栏位，正确的加法是单独加一个 `custom_fields` 字段，把结构化的部分和确实需要自由格式的部分分开放，而不是让整份档案退化成字典。
