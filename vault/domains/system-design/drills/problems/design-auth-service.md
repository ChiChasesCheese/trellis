---
nodes: [problems.foundations.auth-service, security.authn.tokens]
tags: [problem]
---
# Drill: Design an authentication and identity service for hundreds of millions of accounts

Design the identity service every product line at a large company shares: sign-up,
password and passkey login, session/token issuance, SSO for third-party applications, and
account recovery. Assume 500M registered accounts, 150M DAU.

**Constraints to state and honor**
- Token verification is on every API request's hot path: target P99 < 10ms with no network
  round trip to a central store.
- A password change or account lockout must be visible in every region immediately — no
  stale-read window where the old credential still works somewhere.
- Refresh-token rotation must make a stolen token detectable, not just harder to use.
- Account recovery must not be an easier attack surface than the login path it's recovering
  access to.

**Grading points**
- Computes cores needed for the password-hashing tier from a stated work factor and peak
  login QPS, instead of picking a hash algorithm without a throughput budget
  ([[problems-auth-service-hashing-cost-cores]], [[security-password-hashing-params]]).
- Computes token-verification QPS (with internal fan-out) and shows why that number rules
  out a centralized session store as the default hot-path mechanism, choosing stateless JWTs
  instead ([[problems-auth-service-token-verification-qps-forces-stateless]],
  [[security-sessions-vs-jwt]]).
- Separates the credential-of-record store from the refresh-token store by their actual
  write-volume gap, and assigns each its own consistency level
  ([[problems-auth-service-two-stores-two-consistency-levels]]).
- Designs refresh-token rotation so reuse of an already-rotated token is detectable and
  revokes the whole token family ([[problems-auth-service-refresh-rotation-reuse-detection]],
  [[security-refresh-rotation-reuse]]).
- Defends the login endpoint against credential stuffing with fleet-level signals rather
  than per-account lockout, and can say why lockout alone fails
  ([[problems-auth-service-stuffing-fleet-signals-not-lockout]], [[security-credential-stuffing]]).
- Rotates JWT signing keys through an overlap window in JWKS instead of an instant switch
  ([[problems-auth-service-jwks-overlap-window]], [[security-secrets-rotation-live]]).
- Splits SSO/federation by client type — OIDC for consumer clients, SAML for enterprise
  identity providers — instead of forcing one protocol on every integration
  ([[problems-auth-service-oidc-vs-saml-by-client-type]], [[security-oauth-vs-oidc]]).
- Can describe account recovery as sitting behind the same rate-limiting and abuse defenses
  as login, not a separate lenient path ([[problems-auth-service-recovery-shares-rate-limiting]],
  [[security-account-recovery]]).
- At the 10x evolution question, proposes lazy re-hashing on login to migrate password
  parameters instead of a batch job that would spike the hashing tier
  ([[problems-auth-service-lazy-rehash-avoids-batch-spike]]).

**Solution**: [[solution-auth-service]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
