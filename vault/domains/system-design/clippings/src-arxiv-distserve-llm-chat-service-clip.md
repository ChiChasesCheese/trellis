---
title: 'DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large
  Language Model Serving'
source: https://arxiv.org/abs/2401.09670
author: Zhong; Yinmin; Liu; Shengyu; Chen; Junda; Hu; Jianbo; Zhu; Yibo; Xuanzhe;
  Jin; Xin; Zhang; Hao
published: '2024-01-18'
site: arXiv.org
clipped: '2026-09-20'
---

# DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

# Computer Science > Distributed, Parallel, and Cluster Computing

  [Submitted on 18 Jan 2024 (

    [v1](https://arxiv.org/abs/2401.09670v1)), last revised 6 Jun 2024 (this version, v3)]
# Title:DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

[View PDF](/pdf/2401.09670)

[HTML (experimental)](https://arxiv.org/html/2401.09670v3)

            Abstract:DistServe improves the performance of large language models (LLMs) serving by disaggregating the prefill and decoding computation. Existing LLM serving systems colocate the two phases and batch the computation of prefill and decoding across all users and requests. We find that this strategy not only leads to strong prefill-decoding interferences but also couples the resource allocation and parallelism plans for both phases. LLM applications often emphasize individual latency for each phase: time to first token (TTFT) for the prefill phase and time per output token (TPOT) of each request for the decoding phase. In the presence of stringent latency requirements, existing systems have to prioritize one latency over the other, or over-provision compute resources to meet both.

DistServe assigns prefill and decoding computation to different GPUs, hence eliminating prefill-decoding interferences. Given the application's TTFT and TPOT requirements, DistServe co-optimizes the resource allocation and parallelism strategy tailored for each phase. DistServe also places the two phases according to the serving cluster's bandwidth to minimize the communication caused by disaggregation. As a result, DistServe significantly improves LLM serving performance in terms of the maximum rate that can be served within both TTFT and TPOT constraints on each GPU. Our evaluations show that on various popular LLMs, applications, and latency requirements, DistServe can serve 7.4x more requests or 12.6x tighter SLO, compared to state-of-the-art systems, while staying within latency constraints for > 90% of requests.

## Submission history

From: Yinmin Zhong [
[view email](/show-email/f746e30c/2401.09670)]

**Thu, 18 Jan 2024 01:03:38 UTC (141 KB)**

[\[v1\]](/abs/2401.09670v1)
**Tue, 19 Mar 2024 06:20:25 UTC (142 KB)**

[\[v2\]](/abs/2401.09670v2)
**[v3]**Thu, 6 Jun 2024 15:50:51 UTC (273 KB)

### References & Citations

    
    Loading...

# Bibliographic and Citation Tools

            Bibliographic Explorer 

        *(*[What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))
            Connected Papers 

        *(*[What is Connected Papers?](https://www.connectedpapers.com/about))
            Litmaps 

        *(*[What is Litmaps?](https://www.litmaps.co/))
            scite Smart Citations 

        *(*[What are Smart Citations?](https://www.scite.ai/))
# Code, Data and Media Associated with this Article

            alphaXiv 

        *(*[What is alphaXiv?](https://alphaxiv.org/))
            CatalyzeX Code Finder for Papers 

        *(*[What is CatalyzeX?](https://www.catalyzex.com))
            DagsHub 

        *(*[What is DagsHub?](https://dagshub.com/))
            Gotit.pub 

        *(*[What is GotitPub?](http://gotit.pub/faq))
            Hugging Face 

        *(*[What is Huggingface?](https://huggingface.co/huggingface))
            ScienceCast 

        *(*[What is ScienceCast?](https://sciencecast.org/welcome))
# Demos

# Recommenders and Search Tools

              Influence Flower 

          *(*[What are Influence Flowers?](https://influencemap.cmlab.dev/))
              CORE Recommender 

          *(*[What is CORE?](https://core.ac.uk/services/recommender))
# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).
