// Two translation units both define `helper` without `inline`: one-definition-rule violation.
int helper() { return 1; }
