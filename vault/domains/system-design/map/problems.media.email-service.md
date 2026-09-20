%% trellis:begin %%
# Email Service (Gmail)
*Design Problems / Media, Files & Collaboration*

Sending and receiving at scale: SMTP edges, mailbox storage, search, spam and threading.

**Requires:** [[domains/system-design/map/storage.search|Search Indexes]]

## Readings
- [[solution-email-service|设计题解：邮件服务（Email Service，Gmail）]]
- [[src-google-email-service|Email sender guidelines — Gmail Help]]
- [[src-rfc5321-email-service|RFC 5321 — Simple Mail Transfer Protocol]]
- [[src-rfc6376-email-service|RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures]]
- [[src-rfc7208-email-service|RFC 7208 — Sender Policy Framework (SPF)]]
- [[src-rfc7489-email-service|RFC 7489 — Domain-based Message Authentication, Reporting and Conformance (DMARC)]]
- [[src-rfc8620-email-service|RFC 8620 — The JSON Meta Application Protocol (JMAP)]]
- [[src-rfc9051-email-service|RFC 9051 — Internet Message Access Protocol (IMAP) — Version 4rev2]]

## Drills
- [[design-email-service|Drill: Design an email service (Gmail)]]

## Cards (7)
1. [[problems-email-service-attachment-dominates-storage]]
2. [[problems-email-service-immutable-message-mutable-mailboxentry]]
3. [[problems-email-service-spf-dkim-dmarc-distinct-proofs]]
4. [[problems-email-service-per-destination-retry-queue-depth]]
5. [[problems-email-service-per-user-search-sharding-changes-problem]]
6. [[problems-email-service-spam-classifier-fail-open]]
7. [[problems-email-service-quota-protects-tail-not-median]]
%% trellis:end %%

## Notes
