---
id: nr-deep-dive-were-you-there
node: themes.deep-dive
type: qa
---
## Q
Mid-story, the interviewer stops following the narrative and starts drilling: "What was the actual isolation level?" "How did you know it was the GC and not the disk?" What are they doing, and what does a strong answer contain?

## A
They are running an **authenticity check.** Behavioral stories are cheap to embellish and expensive to verify, so the fastest test is to descend below the level a borrowed story can support. It is usually a compliment — nobody drills into a story they have already discounted.

What a strong answer contains, none of it fakeable:

- **A specific instrument.** Not "we profiled it" but "I pulled a flamegraph off the box and the frames were in the allocator."
- **A number you actually saw**, with the shape of the observation. "Pauses were 200ms, but only on two of the twelve nodes."
- **The wrong hypothesis you chased first.** The most convincing detail available, and rehearsed stories never have one.
- **What surprised you.**

Two edge rules. When part of the work was someone else's, **say so immediately and precisely** — volunteering the boundary is a credibility gain, having it discovered is a loss. When you have forgotten a detail, **say what you do remember and how you would re-derive it**: "I do not remember the isolation level; we changed it because we were seeing phantom reads, so it must have been below serializable."
