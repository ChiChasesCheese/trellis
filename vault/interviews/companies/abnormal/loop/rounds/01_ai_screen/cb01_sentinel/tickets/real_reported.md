# REAL: the reported screening question (as the interviewer said it)

(Interviewer, first:) "We have to allow users to suppress some rules. These can be complex rules, like based on geo-ip, which already exists in the code, and other rules."

(A minute later:) "Sorry, I gave you the wrong question. Here's the actual one: the enrichment layer currently hardcodes the threats it looks at — geo-ip, history, and one more. Clients want more configurability without touching platform code. Implement a plugin-based mechanism so that clients never have to change our code."
