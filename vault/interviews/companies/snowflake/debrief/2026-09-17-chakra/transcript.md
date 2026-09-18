# transcript · 2026-09-17_16_34_48.mp3

> mlx-whisper · mlx-community/whisper-large-v3-turbo · 206 segments · 71.1 s

[00:00–00:01] It's not that good.
[00:09–00:09] The
[00:09–00:10] This is the
[00:10–00:10] It's
[00:10–00:10] It's
[00:27–00:27] It's
[00:27–00:27] It's
[00:27–00:27] It's
[00:28–00:29] It's
[00:29–00:29] It's
[00:29–00:29] It's
[00:29–00:29] It's
[00:48–00:51] All right.
[01:04–01:06] Thank you.
[01:35–01:36] Thank you.
[02:01–02:03] Thank you.
[02:37–02:38] Thank you.
[03:04–03:06] Thank you.
[03:35–03:38] Thank you.
[04:07–04:10] Thank you.
[04:33–04:34] Thank you.
[05:27–05:28] We'll see you next time.
[05:30–05:31] Hello hello
[05:32–05:34] Hello hello
[05:34–05:35] Can you hear me?
[05:49–05:51] Hello
[05:51–05:52] Hello
[06:27–06:28] Alright, let's go.
[06:35–06:38] Hey, nice to meet you, the AI officer.
[06:39–06:40] I'm pretty good.
[06:41–06:41] How are you?
[06:49–06:50] Yeah.
[07:08–07:14] I'm currently located in San Jose, California, which is just 20 miles away from your Menlo
[07:14–07:15] Park headquarters.
[07:29–07:40] Yeah, sure, I'm open to all. Actually my preferred location would be Meadow Park or the one in San Francisco if you have.
[07:41–07:43] Yeah, but anyways, open to all.
[07:54–08:05] So now I've already have roughly two years, more specifically 18 months of experience
[08:05–08:09] now since I joined PayPal in 2025 January.
[08:37–08:39] Sorry.
[08:39–08:46] that'll be enough for me and my team. My expected start date will be November, the early stage.
[08:47–08:53] I'm not actively interviewing any company. It's just casually looking forward to new
[08:59–09:00] opportunities.
[09:08–09:17] Well, that is a very interesting topic because my primary coding language right now is Java,
[09:17–09:25] Kovlin, Ruby on Rails, and SQL. Where the SQL, I put it as the last one, but actually
[09:25–09:32] it's the most important one in my day-to-day work because I'm running the SQL in the Snowflake
[09:32–09:40] data warehouse. So what I'm doing right now is just to migrate everything, every computation
[09:40–09:50] logics into an all-in-one data warehouse, which is hosted in Snowglobe, a native Snowflake
[09:50–09:56] platform for all the fee calculation and transactions in PayPal infrastructure.
[10:06–10:21] Yeah, so now I'm the main owner and the builder of the Snowglobe platform, which is a native
[10:21–10:29] snowflake data warehouse and it's it sounds like a data warehouse but actually
[10:29–10:35] it's a distributed platform and backend system as well because if it has
[10:35–10:41] extensibility it can be hosted anywhere to achieve the availability and
[10:41–10:48] consistency and what I'm doing right now is just to build it from zero to one and
[10:48–10:54] migrate the fundings, which is a disbursement system, and pricing, which is a fee calculation
[10:54–11:00] system, and reporting, which is a fee reconciliation and transaction reconciliation system into
[11:00–11:12] this Snowflake-hosted warehouse. To do this, we had to write tons of stored procedures in
[11:12–11:22] native snowflake defined tasks and DAG graphs to try to keep and ledger every single one of rows
[11:22–11:33] of the transactions and fees into the databases and use those rows generated to do the disbursement
[11:33–11:35] and be reconciliation.
[11:37–11:45] The most challenging part for this is that Snowflake SQL is not a very high-level programming
[11:45–11:57] language, but actually, in essence, it can be expressive enough to work the way you want.
[11:57–12:25] So what we are doing is try to learn everything about the native SQL and rewrite all the legacy systems logic in the new platform and achieve the same parity and do all the shadowing monitoring system to make sure that the new legacy system and the new system can work symmetrically.
[12:27–12:28] Yeah, that's pretty much about it.
[12:42–12:54] Well, right now, considering designing as part of the coding, I would say 60% of all my day-to-day work time will be about coding.
[12:54–13:05] And other than that, the 40% lot is mostly about the business and the meetings and to sync up with the other teams to make sure we are on the same page.
[13:06–13:16] Because the Snowflake Data Warehouse is a huge platform across different teams from the upstream to the downstream.
[13:16–13:21] And we need to make sure that our data contracts are in sync.
[13:21–13:23] We are on the same boat with other teammates.
[13:23–13:27] And actually, I'm handling all of this because we are the downstream of the downstream.
[13:28–13:32] We take care of all the fee calculation and disbursement, and we don't want to make any
[13:32–13:35] mistake in this process.
[13:35–13:36] Yeah.
[13:36–13:48] So actually, there are many business side challenges other than, except the coding challenges
[13:48–13:50] are involved in my day-to-day work as well.
[14:02–14:04] Yeah, please, can you repeat your question?
[14:16–14:29] Well, so this is a long story as well, because, well, anyways, I use Cloud Code and Codex
[14:29–14:39] and cursor at the same time. And I also use COCO, which is the snowflake-supported agent
[14:39–14:46] terminal as well. So these are all the coding agents that I utilize in my day-to-day work.
[14:47–14:56] And other than that, because every single agent tool has the rate limit and usage limit
[14:56–15:02] controlled by the company. So I have to have the capability to utilize and harness all of those
[15:02–15:10] agents at the same time, so then I will not run out of usage limit. And also, other than the coding
[15:10–15:19] part, I also developed a very interesting on-call helper for me to ease all the communication
[15:20–15:25] which is named after my name, which is the cheatbot.
[15:26–15:33] So this cheatbot helped me to control all of my sessions across the cloud and codecs
[15:33–15:36] and cursor and other coding agents.
[15:36–15:45] And because all of those sessions information are stored in your own laptop, so my cheatbot
[15:45–15:52] can chronically trigger to pull the latest Slack message and PagerDuty message and Datadog
[15:52–16:03] monitoring systems to understand what happens latest and have me to dive into the specific
[16:03–16:11] session that is about this part of job and then do the automatic development cycle and
[16:11–16:18] then generate the report and outcome and save them as the draft in my slack so
[16:18–16:26] that I can just click send to send this to the related slack threads are the
[16:26–16:35] stakeholders and this is my it's widely adopted in our team and our friend teams
[16:35–16:43] so that everyone in the on-call team are get eased. I'm not sure whether this one is related to your topic,
[16:43–16:49] but I think it's very interesting and challenging and helpful to all the teams and teammates around me.
[17:02–17:12] So I trust AI-generated code based on the collaboration of me and my coding agents and
[17:12–17:21] generate a very detailed plan of all the implementations. So this is step one.
[17:22–17:29] And step two is that I will utilize the test-driven development in all the
[17:29–17:37] phases, so that I can make sure if all the test cases are expected, then I will
[17:37–17:45] maybe put less focus on the implementation details. And then the final
[17:45–17:50] gate is the monitoring system. So the monitoring system including the CI and
[17:50–17:57] you know in the GitHub Actions maybe your code and quality have to pass the CI
[17:57–18:03] threshold and then you can be confident to say that your function works well.
[18:03–18:27] So I think with the adoption of AI, you should focus more on the gates or say the thresholds of your coding standard, of your coding quality and functionality, but instead of the lines of code that you want it to write.
[18:41–18:52] Well, so the first big milestone of our migration to the Snowflake native warehouse is we want
[18:52–18:58] to make sure every single transaction can be dispersed in the next day.
[18:58–19:05] So previously it was T plus 30, means we will charge the fees in the next month instead
[19:06–19:09] of the time we disperse the transaction.
[19:10–19:20] But now we achieve this, and I am responsible for the American Express disbursement and
[19:20–19:21] fee calculation.
[19:21–19:28] So this one is a legacy logic hosted in the Ruby monorepo.
[19:29–19:38] But now, since my first date in this team, I take charge of all the responsibilities
[19:38–19:46] to do this migration because my tech lead and my staff engineer are all on the sabbatical
[19:46–19:46] PTO.
[19:46–19:48] So I had to take care of all of this.
[19:50–19:59] So I built a native Snowflake pipeline from scratch, from the file uploading to the Amazon
[19:59–20:08] S3 to parse all the files and make it independent enough to reduce the file uploads and make
[20:08–20:19] everything unique and then to parse those files into expected format and split into
[20:19–20:28] different tables using the chronicle task triggers and stored procedures and then integrate them into
[20:28–20:36] our Snowflake native pipelines to integrate them together and do the shadowing to make sure that
[20:36–20:44] the new feature and the old feature are in parallel and achieve the same amount of disbursement
[20:44–20:57] and fees. And ultimately, in 2025, it achieved over 100 billion total transaction amount
[20:57–21:01] with no bugs, no accidents, and I'm pretty proud of it.
[21:20–21:30] I am now the main on-call handler and also the closest
[21:30–21:42] membership with our engineers and managers, so I can handle a lot of product and code
[21:42–21:49] accidents. And also because we are under the team, an organization called GreenTree, which
[21:49–21:57] is on par with the Stripe. And we are totally engineer-driven instead of product managers
[21:57–22:07] driven. So that means we need to identify the problems on our own and conduct the experiments
[22:07–22:18] and then do the discovery tickets and implementation and ADR and PRD all on my own. And actually
[22:18–22:25] it's a very challenging job, but it's also very goal-driven, goal-oriented and very suitable
[22:25–22:36] to my personality. I will take this one as an example. In the Snowflake warehouse, we
[22:36–22:46] need to make sure that all of our transactions and fees are reconcilable. To make sure the
[22:46–22:55] PayPal's financial integrity risk team can make sure that our transactions are expected.
[22:55–23:03] They need something to check our quality, right? So make sure that we can meet this expectation.
[23:04–23:13] I conduct and take charge of building a quality gate framework in Snowflake, and it's also
[23:13–23:23] Snowflake native. I conducted the design and meet and think of the external teams to make
[23:23–23:31] sure that I understand their business sense and also make sure that the expected threshold
[23:31–23:38] that they want to meet and then generate a centralized quality gate framework on my own
[23:38–23:43] and express and share this knowledge across the team members.
[23:43–23:48] So then everyone who is building in the Snowflake warehouse
[23:48–23:49] would understand what we are doing
[23:50–23:52] and make it a hard gate to anyone who
[23:52–23:55] want to code and contribute to this repository.
[24:05–24:15] Well, I'm not sure whether this is a little bit off topic. I was an undergrad in construction
[24:15–24:22] management and then I transferred my degree to master's in computer science after my graduation
[24:22–24:32] in China. I always think I am a very goal-oriented person so to achieve that I can finally land
[24:33–24:43] a job in the United States. Also, I am very capable in doing all the challenging work,
[24:43–24:51] so that I can handle all of it on my own and lead the team to build for a new goal.
[24:51–24:57] And also, I was named as a rock star of the organization last year.
[24:57–25:07] And also, my annual review is exceptional, which is the top 5% in our team and our organization.
[25:07–25:16] So I think I've already proved that I have the ability and talent to build amazing infrastructure
[25:16–25:22] and customer-facing product.
[25:22–25:26] But the thing is, I want to do something more.
[25:26–25:33] I don't want to be constrained in a single area, but I want to focus more on the infra.
[25:33–25:42] and the real product that everyone would like to pay to use. So that is the reason why I'm
[25:42–25:50] interested in Snowflake. And as you can see, my daily day-to-day work involves a lot of the
[25:50–25:57] Snowflake and I hope that I can get really involved into the development of this great product.
[26:09–26:17] My first question is, this is the general software engineer position, and do you have
[26:17–26:25] any specific preference over the qualification and quality of the candidates, and if so,
[26:25–26:26] what they are?
[26:27–26:28] Okay.
[27:14–27:22] Yeah, sure. And given that you are an AI interviewer, so I'm pretty interested in
[27:22–27:37] your feedback on me, if that is okay to stay out. Okay, okay, okay, then forget about it.
[27:37–27:47] Then I also have another question, which is the following steps on this interview. So,
[27:47–27:56] So what is your expectation about this position and what you expect from me?
[27:56–28:08] I mean, other than the normal answers, like what is the thing that you value most from
[28:08–28:14] an engineer that has already worked from another company?
[28:20–28:23] Thank you.
[28:56–29:01] I think that's it, thank you so much for your help and your tokens.
[29:15–29:16] Yeah, sure.
[29:16–29:17] See you.
[29:34–29:35] Yeah, bye bye.
[30:06–30:07] Thank you.
