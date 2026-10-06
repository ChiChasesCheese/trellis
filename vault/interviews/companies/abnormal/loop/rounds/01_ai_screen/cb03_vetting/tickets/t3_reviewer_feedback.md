# VET-224 · Learn from reviewer decisions

Security reviewers clear a lot of the candidates we flag, mostly people on a corporate VPN or using
Google Voice legitimately. Use their decisions so we stop re-flagging the same benign patterns.

Reviewers record decisions today with `POST /reviews/<identity_id>/disposition`.
