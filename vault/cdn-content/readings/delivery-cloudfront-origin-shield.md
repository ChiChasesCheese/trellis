---
nodes: [delivery.aws]
url: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html
---
# Amazon CloudFront: Origin Shield

Read this for a concrete AWS tiered-cache design: shield region selection, origin offload, request collapse across edge locations, availability behavior, and the extra request hop. Extract which traffic and origin characteristics make shielding valuable.

Apply the regional and transfer trade-offs to [[delivery-aws-transfer-cost]] and the failure boundaries in [[delivery-aws-failure-boundary]]. The cheapest-looking region is not necessarily the best shield or origin location.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html)
%% trellis:end %%
