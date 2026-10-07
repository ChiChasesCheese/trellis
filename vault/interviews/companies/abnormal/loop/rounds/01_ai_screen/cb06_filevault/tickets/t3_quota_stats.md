# VLT-247: Free tier limits and storage stats

We're launching a free tier: 10 MB per user. Finance also wants to see how much dedup is saving us.

An upload that would put a user over their allowance is rejected with HTTP 413; uploads are also rate
limited per user: HTTP 429 with a `Retry-After` header. Both limits are already in the config.
Users get `GET /stats` (`used_bytes`, `quota_bytes`, `file_count`); admins (`admin_users` in the config)
get `GET /admin/stats` (`logical_bytes`, `physical_bytes`, `saved_bytes`).
