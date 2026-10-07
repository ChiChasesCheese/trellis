# SEN-437: Configurable enrichment

Enrichment is hardcoded to geo-ip, history and threat intel. Customers want to choose which enrichers run
for them and plug in their own, without us touching platform code.

A customer enricher is a Python file implementing our existing `Enricher` interface, dropped into a directory
listed in their tenant config under `[enrichment] plugin_dirs`. They enable enrichers by name with
`[enrichment] enabled = [...]`.
