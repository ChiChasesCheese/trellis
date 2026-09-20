You are putting flashcards in the order a learner should first meet them.

For every topic below you get its cards: id, question, and the start of the
answer. Return the ids of each topic in teaching order. The rules, in order
of precedence:

1. A card that uses a term comes after the card that defines it.
2. What it is → how it works → why it is built that way → where it breaks
   or what it costs → numbers and operations → applying it to a scenario.
3. The plain statement of an idea comes before its edge cases and exceptions.
4. When two cards are independent, the one a practitioner needs more often
   comes first.

Every id of a topic must appear exactly once, under its own topic. Do not
invent, drop, rename or move ids. Output only JSON, in this shape:

{
  "security.authn.tokens": ["<id shown first>", "…"],
  "security.authn.oauth": ["<id shown first>", "…"],
  "security.authn.credentials": ["<id shown first>", "…"],
  …
}

## security.authn.tokens — Sessions & Tokens
Server sessions vs JWTs, access/refresh pairs, rotation and reuse detection, sender-constrained tokens.
- `security-access-refresh-tokens` Q: Why pair a short-lived access token (~5–15 min) with a long-lived refresh token, instead of one long-lived token?
  A: It splits the two jobs a single token can't do at once: - The **access token** is verified statelessly on every request; keeping it short bounds the damage wind
- `security-refresh-rotation-reuse` Q: How does refresh token rotation turn token theft into a detectable event, and what happens on reuse?
  A: **Rotation**: every refresh issues a *new* refresh token and invalidates the one just used — each token is single-use, so a stolen refresh token stops working a
- `security-sender-constrained-tokens` Q: What weakness do bearer tokens have by construction, and how do sender-constrained tokens (DPoP, mTLS-bound) fix it?
  A: A **bearer** token authorizes *whoever holds it* — exfiltrate it (logs, XSS, compromised proxy) and it replays perfectly until expiry. **Sender-constrained** to
- `security-sessions-vs-jwt` Q: Server-side sessions vs JWTs: what does each trade away, and which one makes "log out this user now" hard?
  A: - **Sessions**: opaque id, state in a server store (Redis/DB). Instant revocation — delete the row — but every request costs a store lookup, and the store is sh

## security.authn.oauth — OAuth2 & OIDC
Authorization-code + PKCE flow, what OIDC adds on top, which flow for which client.
- `security-oauth-browser-token-storage` Q: Why was the implicit flow deprecated, and — since code+PKCE replaced it — where should an SPA keep the resulting tokens in 2026?
  A: **Implicit died** because it returned the access token in the **URL fragment**: it leaked into browser history, referrers, logs and extensions; it was unbound (
- `security-oauth-code-pkce` Q: In the OAuth2 authorization code flow, why does the client exchange a code instead of receiving tokens directly in the redirect — and what does PKCE add?
  A: The redirect travels through the **browser** (URL, history, referrers, extensions) — an untrusted channel. The short-lived, one-time **code** is useless there b
- `security-oauth-grant-selection` Q: Pick the grant: (a) a nightly batch job calling a partner API, (b) a web app acting for a signed-in user, (c) a smart TV app. What makes (a) fundamentally different from the others?
  A: - (a) **Client credentials** — the app authenticates *as itself* with a secret or (better) mTLS / signed JWT assertion. - (b) **Authorization code + PKCE** — a 
- `security-oauth-scopes-vs-audience` Q: Scopes vs audience: what does each one constrain, and why is "the token has scope `orders:read`, so let the request through" an authorization bug?
  A: - **Scope** = *what the user delegated to this client* — a coarse, consent-visible capability (`orders:read`). It only ever **narrows** what the client may ask 
- `security-oauth-vs-oidc` Q: "Log in with Google" — is that OAuth2 or OIDC, and why is using a plain OAuth2 access token as proof of identity a bug?
  A: That's **OIDC** — an identity layer on top of OAuth2. OAuth2 alone answers "may this app access this resource?" (**delegation**); it says nothing about who the 

## security.authn.credentials — Passwords & Passkeys
Credential storage, phishing resistance, and the WebAuthn/passkey model.
- `security-account-recovery` Q: You ship passkey-only login. Why is your account's real security level probably still "SMS", and how do you design recovery?
  A: An account is only as strong as its **weakest path to a session**. Attackers don't break the passkey — they run the "lost my device" flow. If recovery is an ema
- `security-credential-stuffing` Q: Credential stuffing vs brute force: why does per-account rate limiting barely help, and what actually detects it?
  A: Brute force is *many guesses against one account*; **stuffing replays leaked username+password pairs across millions of accounts** — typically **one or two atte
- `security-passkeys-phishing` Q: Why are passkeys (WebAuthn) phishing-resistant when passwords + TOTP codes are not?
  A: Password and TOTP are **user-typeable secrets** — a fake site can ask for them and relay them to the real site in real time (proxy phishing defeats OTP). Passke
- `security-password-hashing-params` Q: You must store user passwords and also verify high-entropy API keys. Which algorithm and parameters for each, and why are they different?
  A: **Passwords — a slow, memory-hard KDF.** Argon2id is the default (OWASP baseline ~19 MiB memory, t=2, p=1); bcrypt cost ≥ 12 is acceptable legacy (watch its 72-
- `security-webauthn-ceremony` Q: At a systems level: what does your server store per passkey, and what must it verify on each login ceremony?
  A: **Registration** — server issues a random **challenge**; the authenticator generates a keypair scoped to your **RP ID** and returns the public key. You persist:

## security.authz — Authorization & API Security
RBAC vs ABAC, API keys vs user tokens, TLS everywhere, secrets handling.
- `security-api-keys-vs-user-tokens` Q: API keys vs user tokens: what does each identify, and why must a multi-tenant API never authorize on the key alone?
  A: - **API key**: identifies an **application/tenant** — long-lived, no user context, ideal for server-to-server calls, metering, and rate limiting per customer. S
- `security-confused-deputy` Q: An internal reporting service with read access to *all* tenants' data serves any caller that asks. A low-privilege client requests another tenant's report and gets it. Name the vulnerability class and the fix.
  A: **Confused deputy**: a privileged service is tricked into using *its own* authority on behalf of a less-privileged caller. Classic instances: internal services 
- `security-mtls-vs-tokens-s2s` Q: For service-to-service auth, mTLS and signed tokens (JWTs) are often used *together*. What does each prove that the other cannot?
  A: - **mTLS** proves **workload identity at the channel level**: "this connection really is from billing-service" (cert issued via SPIFFE/mesh CA), plus encryption
- `security-rbac-vs-abac` Q: When does RBAC stop being enough and force a move toward ABAC (or relationship-based) authorization?
  A: RBAC (user → roles → permissions) breaks when the decision depends on **context the role can't encode**: - **Resource ownership/relationships**: "editors can ed
- `security-secrets-handling` Q: Where do service credentials (DB passwords, API keys) live in a well-designed 2026 system, and what beats static secrets entirely?
  A: - Never in code, images, or plain env files — those leak via repos, logs, and crash dumps. - **Secret manager** (Vault, AWS/GCP Secrets Manager): centralized st
- `security-secrets-rotation-live` Q: How do you rotate a database password or a JWT signing key without restarting services or dropping a single request?
  A: Never flip atomically — rotate with an **overlap window** where two versions are valid: - **Consumed secrets** (DB passwords): create the new credential *alongs
