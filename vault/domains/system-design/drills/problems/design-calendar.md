---
nodes: [problems.realtime.calendar, storage.relational.indexing]
tags: [problem]
---
# Drill: Design a calendar and scheduling system like Google Calendar

Design the event/attendee model, recurring events, free/busy queries, invitations and
client sync for a calendar system: 300 million registered accounts, 60 million daily
active users, recurring events that must not be stored as individually materialized rows,
and external attendees on other calendar products.

**Constraints to state and honor**
- 60,000,000 DAU with a computed RSVP-write peak of about 2,083 QPS (using a business-
  hours-concentrated ×4 peak factor) and a relational-primary ceiling assumption of about
  3,000 conditional updates/sec.
- 6,000,000 recurring event series created/day, each averaging about 2 years (730
  occurrences) before ending.
- Free/busy queries must return only availability, never event details, and must handle
  multiple attendees within a low read-latency budget.
- Invitations must reach attendees on calendar products this system does not control,
  using an open interoperability standard rather than a bespoke per-product integration.

**Grading points**
- Computes the RSVP-write peak against the assumed relational-primary ceiling, states the
  resulting safety margin, and argues what that margin forces in the attendee-state
  storage design ([[problems-calendar-rsvp-write-margin]]).
- Computes the storage cost of materializing every recurring occurrence as its own row
  versus storing one recurrence rule per series, and explains why an unbounded series
  makes the rule-based approach necessary rather than just cheaper
  ([[problems-calendar-recurring-storage-blowup]]).
- Splits an event's organizer-controlled core fields and its per-attendee state into two
  separate tables/entities rather than embedding attendees in the event record, and can
  explain the write-contention problem this avoids ([[problems-calendar-event-attendee-split]]).
- Stores a recurring event's time as local time plus an IANA time zone identifier rather
  than a precomputed UTC instant, and can justify it with a concrete example of time zone
  rules changing over time ([[problems-calendar-tzid-not-utc]]).
- Designs free/busy queries against a per-user range index of busy intervals, returning
  only busy/free state, and explains why this is a deliberate permission boundary and not
  just a performance optimization ([[problems-calendar-freebusy-permission-boundary]]).
- Designs external-attendee invitations using an open interoperability protocol (iTIP)
  rather than bespoke per-product integrations, and can explain how an edited event is
  recognized as an update rather than a new invitation ([[problems-calendar-itip-external-interop]]).
- States what happens when a client's sync token is no longer valid, and can describe at
  least one real protocol's specific invalidation behavior ([[problems-calendar-sync-token-invalidation]]).
- States what happens to the attendee-write safety margin at 10x DAU and what concrete
  storage-sharding change this forces ([[problems-calendar-10x-attendee-sharding]]).

**Solution**: [[solution-calendar]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
