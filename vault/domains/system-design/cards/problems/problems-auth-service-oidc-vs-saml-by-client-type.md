---
id: problems-auth-service-oidc-vs-saml-by-client-type
node: problems.foundations.auth-service
type: qa
step: 7
tags: [grown]
---
## Q
In an identity service offering SSO to third-party applications, why is picking either OIDC-only or SAML-only for every client the wrong call, and what determines which protocol a given client gets?

## A
SAML-only excludes the consumer-facing OAuth/OIDC ecosystem almost every individual-user identity provider (Google, Apple, etc.) speaks natively, while its XML-based assertions are heavier than most consumer clients need. OIDC-only excludes enterprise customers whose identity providers (Okta, AD FS) are built around SAML's richer attribute-bearing assertions and established federation metadata exchange. The split is by client type: consumer-facing and modern applications get OIDC (OAuth2 + an ID token, verified via its `aud` and `nonce`), enterprise SSO customers get SAML (assertion signature and Audience/Recipient checks), and both are normalized internally into the same local identity record — the service doesn't force one protocol on a client population it wasn't designed for.

## Q zh
在一个为第三方应用提供 SSO 的身份服务里，为什么对所有客户端只用 OIDC 或只用 SAML 都是错误选择，什么决定了某个客户端用哪种协议？

## A zh
只用 SAML 会排除几乎所有面向个人用户的身份提供商（Google、Apple 等）原生使用的消费级 OAuth/OIDC 生态，而它基于 XML 的断言对大多数消费级客户端来说也过重。只用 OIDC 会排除企业客户——他们的身份提供商（Okta、AD FS）围绕 SAML 更丰富的属性携带断言和成熟的联邦元数据交换构建。正确的划分按客户端类型：消费级和现代应用用 OIDC（OAuth2 + ID token，校验其 `aud` 和 `nonce`），企业 SSO 客户用 SAML（断言签名和 Audience/Recipient 校验），两者在内部统一归一成同一份本地身份记录——服务不会把一种协议强加给它本不是为其设计的客户群体。
