---
id: security-request-integrity-message-length
node: security-cost.request-integrity
type: qa
---
## Q
The edge proxy and origin disagree on a request containing both `Content-Length` and `Transfer-Encoding`. What class of failure can result, and what is the defense?

## A
Request smuggling: the two parsers can disagree on message boundaries, letting attacker-controlled bytes become another user's request or bypass routing policy. Reject ambiguous framing, normalize once, use protocol-compliant libraries, and test edge-to-origin parser pairs with malformed and duplicate headers. Hiding one header after a parser has already framed the stream is too late.

## Q zh
edge proxy 与 origin 对同时包含 `Content-Length` 和 `Transfer-Encoding` 的 request 解释不同。会导致哪类 failure，如何防御？

## A zh
会导致 request smuggling：两个 parser 对 message boundary 的判断不同，使 attacker-controlled byte 成为另一个用户的 request，或绕过 routing policy。应 reject ambiguous framing、只 normalization 一次、使用 protocol-compliant library，并用 malformed 与 duplicate header 测试 edge-to-origin parser pair。parser 已完成 stream framing 后再隐藏某个 header 已经太晚。
