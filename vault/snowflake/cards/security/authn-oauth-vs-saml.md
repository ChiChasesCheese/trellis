---
id: authn-oauth-vs-saml
node: security.authn-mfa-sso
type: qa
tags: [grown]
---
## Q
BI 工具（如 Tableau）代表终端用户访问 Snowflake 时，为什么通常用 OAuth 而不是让工具保存每个用户的密码？

## A
OAuth 是授权委托协议：用户在授权服务器（Snowflake 自带的 Snowflake OAuth，或外部的 External OAuth 如 Okta、Azure AD）处登录一次，第三方应用拿到一个有有效期、可限定作用范围（scope，如某个角色）的访问令牌（access token），用令牌而非密码访问 Snowflake。应用从不接触密码，令牌过期或被吊销即失效，而且查询仍以真实用户身份执行，审计和权限都按个人计算。
