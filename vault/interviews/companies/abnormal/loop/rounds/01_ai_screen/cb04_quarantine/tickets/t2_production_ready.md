# QRN-231: Make quarantine production-ready

We're turning this on for our largest customer next week. Make it production-ready — your call on what
matters most.

Ops will run a cron job to deliver receipts to reporters: `python -m quarantine drain-outbox`.
