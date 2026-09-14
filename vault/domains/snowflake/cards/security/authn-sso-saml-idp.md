---
id: authn-sso-saml-idp
node: security.authn-mfa-sso
type: qa
tags: [grown]
---
## Q
企业希望员工用公司的 Okta / Azure AD 账号登录 Snowflake，离职时在 IdP（身份提供方）一处禁用即可。联合单点登录（federated SSO，基于 SAML 2.0）是怎么做到这点的？

## A
Snowflake 作为 SAML 的服务提供方（SP），把登录重定向到外部 IdP；IdP 完成认证（包括它自己的 MFA 策略）后签发一个签名的 SAML 断言（assertion），Snowflake 验证签名并把断言中的身份映射到 Snowflake 用户。密码和 MFA 都由 IdP 管理，因此在 IdP 禁用账号就立即切断新的登录。配合 SCIM 还可以自动同步用户与角色的创建和删除。
