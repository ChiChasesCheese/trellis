---
id: cc-output-sentinels-null-vs-empty
node: output.sentinels
type: cloze
---
Two different absences need two different byte sequences: a point-in-time lookup with no value at or before `t` prints {{c1::`null`}} — there is no value — while a query that legitimately returns an empty collection prints {{c2::an empty line}}, because there *is* an answer and it is nothing. Confusing them fails tests in {{c3::both}} directions. An expired newest version must print the "no value" form rather than {{c4::falling back to the previous version}}.

## zh
两种不同的「没有」需要两种不同的字节：某个时间点查询在 `t` 或之前没有任何值时，打印 {{c1::`null`}} —— 不存在值；而合法地返回空集合的查询打印 {{c2::一个空行}}，因为答案*是*存在的，只不过是空的。把两者搞混会在 {{c3::两个}} 方向上挂测试。最新版本已过期时必须打印「无值」形式，而不是 {{c4::回退到上一个版本}}。
