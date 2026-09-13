---
id: delivery-compatibility-unknown-config
node: delivery.compatibility
type: qa
---
## Q
An older proxy receives a config containing a new cache directive it does not understand. Should it ignore the field?

## A
Only if the schema declares that omission preserves safety. For correctness or authorization fields, reject the config or choose a fail-safe behavior such as bypassing shared cache; silent ignore can create inconsistent policy across the fleet. Validate config before publication, expose applied versus desired version, and design unknown-field semantics explicitly.

## Q zh
旧 proxy 收到包含新 cache directive、但自身无法理解的 config。它应该 ignore 该 field 吗？

## A zh
只有 schema 明确声明 omission 仍保持安全时才可以。对于 correctness 或 authorization field，应 reject config，或选择 fail-safe behavior，例如 bypass shared cache；silent ignore 会造成 fleet policy 不一致。发布前验证 config，暴露 applied 与 desired version，并明确设计 unknown-field semantics。
