---
slug: reformat-date
---
## Q
**LC 1507 转变日期格式**｜Easy

日期形如 `"20th Oct 2052"`（日带序数后缀，月是三字母英文缩写）。把它转成 `YYYY-MM-DD` 格式。

## A
**一句话。** 按空格拆成三段，月份缩写在列表里的位置加 1 就是月，日去掉末两位后缀，年原样，再用零填充格式化。

```python
def reformat_date(date):
    day, month, year = date.split()
    months = ("Jan Feb Mar Apr May Jun "
              "Jul Aug Sep Oct Nov Dec").split()
    return (f"{year}-{months.index(month) + 1:02d}"
            f"-{int(day[:-2]):02d}")
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 月份下标忘了加 1：`Jan` 在列表里是 0，对应 1 月。
- 日不补零：`1st` 要变成 `01`，用 `:02d`。
- 去后缀时只截一位：`st/nd/rd/th` 都是两位字母。

**追问。**
- 不想手写月份表？：`datetime.strptime` 可以直接解析，但日的序数后缀要先自己去掉。
- 输入可能乱序？：先校验三段的形态，再按各自规则解析。

**同模式。** LC 1360 日期之间隔几天、LC 1154 一年中的第几天、LC 1185 一周中的第几天
