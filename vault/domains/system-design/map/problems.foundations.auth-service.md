%% trellis:begin %%
# Authentication & Identity Service
*Design Problems / Building Blocks & Warm-ups*

Sign-up, login, sessions vs tokens, SSO and revocation for hundreds of millions of accounts.

**Requires:** [[domains/system-design/map/security.authn.tokens|Sessions & Tokens]]

## Readings
- [[solution-auth-service|设计题解：身份认证服务（Authentication & Identity Service）]]
- [[src-auth0-refresh-rotation-auth-service|Refresh Token Rotation]]
- [[src-nist-800-63b-auth-service|NIST SP 800-63B — Digital Identity Guidelines: Authentication and Lifecycle Management]]
- [[src-owasp-password-storage-auth-service|Password Storage Cheat Sheet]]
- [[src-rfc9700-auth-service|RFC 9700 — Best Current Practice for OAuth 2.0 Security]]
- [[src-webauthn-w3c-auth-service|Web Authentication: An API for accessing Public Key Credentials Level 3]]

## Drills
- [[design-auth-service|Drill: Design an authentication and identity service for hundreds of millions of accounts]]

## Cards (9)
1. [[problems-auth-service-hashing-cost-cores]]
2. [[problems-auth-service-token-verification-qps-forces-stateless]]
3. [[problems-auth-service-two-stores-two-consistency-levels]]
4. [[problems-auth-service-refresh-rotation-reuse-detection]]
5. [[problems-auth-service-stuffing-fleet-signals-not-lockout]]
6. [[problems-auth-service-jwks-overlap-window]]
7. [[problems-auth-service-oidc-vs-saml-by-client-type]]
8. [[problems-auth-service-lazy-rehash-avoids-batch-spike]]
9. [[problems-auth-service-recovery-shares-rate-limiting]]
%% trellis:end %%

## Notes
