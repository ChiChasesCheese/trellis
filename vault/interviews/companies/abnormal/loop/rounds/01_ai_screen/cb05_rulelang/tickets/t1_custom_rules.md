# RUL-208: Customer-defined detection rules

Customers want to write their own detection rules without waiting on us, e.g.
`sender.domain_age_days < 7 and any(link.host in intel.bad_hosts)`. Let them.

Customers define them per tenant in their tenant config, under `[rules]`, as `<rule name> = "<expression>"`.
When a rule matches an event, that should show up like any other detection on that event.
