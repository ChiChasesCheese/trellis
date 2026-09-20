---
title: Reducing Instagram’s basic video compute time by 94 percent
source: https://engineering.fb.com/2022/11/04/video-engineering/instagram-video-processing-encoding-reduction/
author: Ryan Peterman; Haixia Shi
published: '2022-11-04'
site: Engineering at Meta
clipped: '2026-09-20'
---

# Reducing Instagram’s basic video compute time by 94 percent

- In our constant quest to [prioritize efficiency](https://engineering.fb.com/2019/03/14/data-center-engineering/accelerating-infrastructure/) , Instagram’s engineers have developed a way to process new videos that reduces the cost to produce basic video encodings by 94 percent.
- With this method in place, [Meta’s video infrastructure](https://engineering.fb.com/2021/04/05/video-engineering/how-facebook-encodes-your-videos/) can continue to scale without needing to add more machines.
- This frees up resources so more people can watch advanced encodings, which provide clearer video that plays more smoothly. This is especially beneficial for people in countries that have slower internet connections.

Instagram’s growing user base of more than 2 billion monthly active users requires us to get the best possible performance from our fleet of servers. In early 2021, we ran projections that showed that within 12 months we would not have enough capacity to provide video uploads for everyone. But in our never-ending quest to prioritize efficiency, we uncovered a way to handle this increasing demand and [scale our infrastructure](https://engineering.fb.com/2022/09/06/data-center-engineering/viewing-the-world-as-a-computer-global-capacity-management/) by doing more with the machines we already have. 

Instagram creates multiple encoded versions of uploaded videos, each with different characteristics. By repurposing one type of video encoding to help generate another type, we reduced the compute resources we spend on less-watched video encodings by 94 percent. With more resources available, we can produce more advanced encodings — allowing more people to experience clearer video with smoother playback.

## Where Instagram spends video compute

We generate two types of video encoding for each video uploaded to Instagram:

1. **Minimum functionality encodings** are compatible with all Instagram clients. Their lower-efficiency compression is easier for older devices to decode and play.
2. **Advanced encodings** use[newer compression technologies](https://engineering.fb.com/2018/04/10/video-engineering/av1-beats-x264-and-libvpx-vp9-in-practical-use-case/) for higher-quality playback. In the example below, close-ups of two video frames show that we can provide sharper detail with fewer bits (note the clarity of the video on the right compared with that on the left).

The problem was that we were spending more than 80 percent of our resources processing minimum functionality encodings. If we stayed on that trajectory, minimum functionality would monopolize our resources within a year. As a result, videos would start to take longer to publish — or fail to publish altogether. Our advanced encodings covered only 15 percent of total watch time, and we projected that spending all our compute on minimum functionality versions would soon prevent us from being able to provide advanced video encoding watch time.

## Removing redundant workloads

Instagram creates two classes of minimum functionality encodings. For every video, we generate basic adaptive bit rate (ABR) encodings — our most-watched minimum functionality type. For the steadiest playback, clients can select the version that best fits their connection speed to prevent stalling caused by changes in bandwidth — a technique called [adaptive bit rate streaming](https://howvideo.works/#adaptive-bitrate-streaming).

We rarely deliver progressive encodings, the other minimum functionality type, but we continue to produce them to maintain compatibility with old versions of the Instagram app that don’t support ABR playback.

Traditionally, we have created both ABR and progressive encodings from the original file the client uploaded to our back end. But this process hogs compute resources: As the following terminal command shows, it takes 86.17 seconds of CPU time to transcode a 23-second video to 720p.

```
$ time ffmpeg -i input.mp4 -vf scale=-1:720 -c:v libx264 output.mp4
86.17s user 1.32s system 964% cpu 9.069 total
```
We noticed that the settings of the two sets of encodings were similar. They used the same codec with only minor differences in the encoding profile and preset. Then it dawned on us: We could **replace our basic ABR encodings with the progressive encodings’ video frames by repackaging them into an ABR-capable file structure**. This would virtually eliminate the cost of generating our basic ABR encodings. The following terminal command times show that it takes only 0.36 seconds to generate a manifest file and repackage the video frames into an ABR-capable file structure for the same input video.

```
$ time MP4Box -add input.mp4 -dash 2000 -profile dashavc264:onDemand -out manifest.mpd 
video_output.mp4
0.36s user 2.22s system 95% cpu 2.690 total
```
This approach frees up compute for advanced encoding production, although it comes at the expense of the compression efficiency of our basic ABR encodings. Our theory was that **generating a greater number of advanced encodings would be a net positive for people who use Instagram.**

## Building a framework to test our theory

We needed to prove our theory before we could ship to production. If we compared the basic ABR encodings before and after our change, we would see only regressions. We also needed to measure the net effect from more advanced encodings. The diagram below shows the higher watch time we expected for advanced encodings after freeing up compute from our basic ABR. This would make up for the poorer compression efficiency of the new basic ABR.

To measure this, we built a testing framework that replicated some small percentage of traffic across a test pool and a control pool of equal processing power. We saved the encodings from each pool to different namespaces so we could later identify them as part of the control or test catalog of videos. Then, at delivery time, people would see encodings from only one catalog or the other. This would allow us to measure whether the new encoding scheme was better.

From this test, we proved that although we were degrading the compression efficiency of the basic ABR encodings in the test pool, the higher watch time for advanced encodings more than made up for it.

## Pushing to production

After we launched this optimization, we saw major gains in compute savings and higher advanced encoding watch time. **Our new encoding scheme reduced the cost of generating our basic ABR encodings by 94 percent.** With more resources available, we were able to increase the overall watch time coverage of advanced encodings by 33 percent. This means that today more people on Instagram get to experience clearer video that plays more smoothly. This is especially important in providing a great experience to people in countries that have slower internet connections.

There is still more engineering innovation needed, as Instagram’s growing user base will continue to place increasing demand on our fleet of servers. Stay tuned!

Over the years, Instagram has worked continuously to i[mprove its product offerings](https://engineering.fb.com/2022/10/31/ml-applications/instagram-notification-management-machine-learning/). Given our scale — including 2 billion monthly active users on our platform and more than 140 billion Reels plays across Instagram and Facebook every day — our work can make a huge impact. If this sounds interesting to you, [join us!](https://www.facebookcareers.com/jobs/?is_leadership=0&teams%5B0%5D=Software%20Engineering&is_in_page=0)

## Acknowledgments

*Thanks to Haixia Shi for incepting the idea for this efficiency optimization. Thanks to Richard Shyong for implementing the optimization and the testing framework, which enables us to measure all compute efficiency investments. Thanks to Runshen Zhu and Ang Li for discussions that resulted in the investment in this scope. Thanks to our partners Atasay Gokkaya, Justin Li, Chia-I Wei, and Zainab Zahid for helping with testing pool provisioning and discussions on video compute efficiency.*
