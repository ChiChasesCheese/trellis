---
nodes: [reliability.slos, reliability.alerting, reliability.incidents]
url: https://sre.google/sre-book/service-level-objectives/
---
# Google SRE: Service Level Objectives

Read this to replace infrastructure health with a user-centered reliability contract. Extract how to choose SLIs, define an objective and measurement window, and use the resulting error budget to decide whether a risky release can continue.

While reading, connect the contract to [[reliability-slos-user-centered-sli]], [[reliability-slos-error-budget-release]], and [[reliability-alerting-multiwindow-burn]]. The incident value is the shared definition of “bad”: mitigation and recovery should be judged against the same user outcome used before the incident.

%% trellis:begin %%
## Source
[Open the original ↗](https://sre.google/sre-book/service-level-objectives/)
%% trellis:end %%
