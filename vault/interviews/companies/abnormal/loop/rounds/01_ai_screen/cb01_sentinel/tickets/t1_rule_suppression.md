# SEN-412: Let customers suppress detections

Customers keep asking us to mute specific detections. Example: impossible-travel alerts for staff who work
through a corporate VPN whose egress is in another country. Let customers suppress rules.

Customers manage this through the API: `POST /suppressions` (body has a `rule_id`, and optionally match
conditions, e.g. `{"rule_id": "impossible_travel", "match": {"geo.country": "DE"}}`), `GET /suppressions`
and `DELETE /suppressions/<id>`.
