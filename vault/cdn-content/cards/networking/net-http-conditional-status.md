---
id: net-http-conditional-status
node: networking.http-semantics
type: qa
---
## Q
A client sends `If-None-Match` and the representation is unchanged. Why should the server return `304` rather than `200` with an empty body?

## A
`304 Not Modified` has defined conditional-request semantics: the client reuses its stored representation and updates metadata from the 304. A `200` means a selected representation was returned and participates differently in caches; sending it empty risks replacing valid content. Status codes are protocol behavior, not cosmetic labels.

## Q zh
client 发送 `If-None-Match`，representation 没变化。为什么 server 应返回 `304`，而不是 body 为空的 `200`？

## A zh
`304 Not Modified` 有明确 conditional-request semantics：client 复用已存 representation，并用 304 更新 metadata。`200` 表示返回了一个选定 representation，在 cache 中行为不同；空 `200` 甚至可能替换掉有效内容。status code 是 protocol behavior，不是装饰标签。
