# turns · AI vs me（启发式标注，错了写 speakers.json 再跑）

### 00 · me · 00:48–00:51 · 2.8 s · 2 words · segs 46–46

All right.

### 01 · me · 05:30–05:35 · 5.4 s · 6 words · segs 56–58

Hello hello Can you hear me?

### 02 · me · 05:49–05:52 · 3.0 s · 2 words · segs 59–60

Hello Hello

### 03 · me · 06:27–06:28 · 1.0 s · 3 words · segs 61–61

Alright, let's go.

### 04 · me · 06:35–06:41 · 6.0 s · 14 words · segs 62–64

Hey, nice to meet you, the AI officer. I'm pretty good. How are you?

### 05 · me · 06:49–06:50 · 0.7 s · 1 words · segs 65–65

Yeah.

### 06 · me · 07:08–07:15 · 7.8 s · 18 words · segs 66–67

I'm currently located in San Jose, California, which is just 20 miles away from your Menlo Park headquarters.

### 07 · me · 07:29–07:43 · 14.0 s · 29 words · segs 68–69

Yeah, sure, I'm open to all. Actually my preferred location would be Meadow Park or the one in San Francisco if you have. Yeah, but anyways, open to all.

### 08 · me · 07:54–08:09 · 15.3 s · 22 words · segs 70–71

So now I've already have roughly two years, more specifically 18 months of experience now since I joined PayPal in 2025 January.

### 09 · me · 08:39–08:53 · 14.0 s · 31 words · segs 73–74

that'll be enough for me and my team. My expected start date will be November, the early stage. I'm not actively interviewing any company. It's just casually looking forward to new

### 10 · me · 09:08–09:56 · 47.5 s · 95 words · segs 76–81

Well, that is a very interesting topic because my primary coding language right now is Java, Kovlin, Ruby on Rails, and SQL. Where the SQL, I put it as the last one, but actually it's the most important one in my day-to-day work because I'm running the SQL in the Snowflake data warehouse. So what I'm doing right now is just to migrate everything, every computation logics into an all-in-one data warehouse, which is hosted in Snowglobe, a native Snowflake platform for all the fee calculation and transactions in PayPal infrastructure.

### 11 · me · 10:06–12:28 · 141.8 s · 245 words · segs 82–96

Yeah, so now I'm the main owner and the builder of the Snowglobe platform, which is a native snowflake data warehouse and it's it sounds like a data warehouse but actually it's a distributed platform and backend system as well because if it has extensibility it can be hosted anywhere to achieve the availability and consistency and what I'm doing right now is just to build it from zero to one and migrate the fundings, which is a disbursement system, and pricing, which is a fee calculation system, and reporting, which is a fee reconciliation and transaction reconciliation system into this Snowflake-hosted warehouse. To do this, we had to write tons of stored procedures in native snowflake defined tasks and DAG graphs to try to keep and ledger every single one of rows of the transactions and fees into the databases and use those rows generated to do the disbursement and be reconciliation. The most challenging part for this is that Snowflake SQL is not a very high-level programming language, but actually, in essence, it can be expressive enough to work the way you want. So what we are doing is try to learn everything about the native SQL and rewrite all the legacy systems logic in the new platform and achieve the same parity and do all the shadowing monitoring system to make sure that the new legacy system and the new system can work symmetrically. Yeah, that's pretty much about it.

### 12 · me · 12:42–13:50 · 67.9 s · 159 words · segs 97–107

Well, right now, considering designing as part of the coding, I would say 60% of all my day-to-day work time will be about coding. And other than that, the 40% lot is mostly about the business and the meetings and to sync up with the other teams to make sure we are on the same page. Because the Snowflake Data Warehouse is a huge platform across different teams from the upstream to the downstream. And we need to make sure that our data contracts are in sync. We are on the same boat with other teammates. And actually, I'm handling all of this because we are the downstream of the downstream. We take care of all the fee calculation and disbursement, and we don't want to make any mistake in this process. Yeah. So actually, there are many business side challenges other than, except the coding challenges are involved in my day-to-day work as well.

### 13 · me · 14:02–14:04 · 2.7 s · 7 words · segs 108–108

Yeah, please, can you repeat your question?

### 14 · me · 14:16–16:49 · 152.8 s · 306 words · segs 109–127

Well, so this is a long story as well, because, well, anyways, I use Cloud Code and Codex and cursor at the same time. And I also use COCO, which is the snowflake-supported agent terminal as well. So these are all the coding agents that I utilize in my day-to-day work. And other than that, because every single agent tool has the rate limit and usage limit controlled by the company. So I have to have the capability to utilize and harness all of those agents at the same time, so then I will not run out of usage limit. And also, other than the coding part, I also developed a very interesting on-call helper for me to ease all the communication which is named after my name, which is the cheatbot. So this cheatbot helped me to control all of my sessions across the cloud and codecs and cursor and other coding agents. And because all of those sessions information are stored in your own laptop, so my cheatbot can chronically trigger to pull the latest Slack message and PagerDuty message and Datadog monitoring systems to understand what happens latest and have me to dive into the specific session that is about this part of job and then do the automatic development cycle and then generate the report and outcome and save them as the draft in my slack so that I can just click send to send this to the related slack threads are the stakeholders and this is my it's widely adopted in our team and our friend teams so that everyone in the on-call team are get eased. I'm not sure whether this one is related to your topic, but I think it's very interesting and challenging and helpful to all the teams and teammates around me.

### 15 · me · 17:02–18:27 · 85.0 s · 160 words · segs 128–136

So I trust AI-generated code based on the collaboration of me and my coding agents and generate a very detailed plan of all the implementations. So this is step one. And step two is that I will utilize the test-driven development in all the phases, so that I can make sure if all the test cases are expected, then I will maybe put less focus on the implementation details. And then the final gate is the monitoring system. So the monitoring system including the CI and you know in the GitHub Actions maybe your code and quality have to pass the CI threshold and then you can be confident to say that your function works well. So I think with the adoption of AI, you should focus more on the gates or say the thresholds of your coding standard, of your coding quality and functionality, but instead of the lines of code that you want it to write.

### 16 · me · 18:41–21:01 · 140.2 s · 249 words · segs 137–155

Well, so the first big milestone of our migration to the Snowflake native warehouse is we want to make sure every single transaction can be dispersed in the next day. So previously it was T plus 30, means we will charge the fees in the next month instead of the time we disperse the transaction. But now we achieve this, and I am responsible for the American Express disbursement and fee calculation. So this one is a legacy logic hosted in the Ruby monorepo. But now, since my first date in this team, I take charge of all the responsibilities to do this migration because my tech lead and my staff engineer are all on the sabbatical PTO. So I had to take care of all of this. So I built a native Snowflake pipeline from scratch, from the file uploading to the Amazon S3 to parse all the files and make it independent enough to reduce the file uploads and make everything unique and then to parse those files into expected format and split into different tables using the chronicle task triggers and stored procedures and then integrate them into our Snowflake native pipelines to integrate them together and do the shadowing to make sure that the new feature and the old feature are in parallel and achieve the same amount of disbursement and fees. And ultimately, in 2025, it achieved over 100 billion total transaction amount with no bugs, no accidents, and I'm pretty proud of it.

### 17 · me · 21:20–23:55 · 154.5 s · 278 words · segs 156–175

I am now the main on-call handler and also the closest membership with our engineers and managers, so I can handle a lot of product and code accidents. And also because we are under the team, an organization called GreenTree, which is on par with the Stripe. And we are totally engineer-driven instead of product managers driven. So that means we need to identify the problems on our own and conduct the experiments and then do the discovery tickets and implementation and ADR and PRD all on my own. And actually it's a very challenging job, but it's also very goal-driven, goal-oriented and very suitable to my personality. I will take this one as an example. In the Snowflake warehouse, we need to make sure that all of our transactions and fees are reconcilable. To make sure the PayPal's financial integrity risk team can make sure that our transactions are expected. They need something to check our quality, right? So make sure that we can meet this expectation. I conduct and take charge of building a quality gate framework in Snowflake, and it's also Snowflake native. I conducted the design and meet and think of the external teams to make sure that I understand their business sense and also make sure that the expected threshold that they want to meet and then generate a centralized quality gate framework on my own and express and share this knowledge across the team members. So then everyone who is building in the Snowflake warehouse would understand what we are doing and make it a hard gate to anyone who want to code and contribute to this repository.

### 18 · me · 24:05–25:57 · 112.0 s · 228 words · segs 176–189

Well, I'm not sure whether this is a little bit off topic. I was an undergrad in construction management and then I transferred my degree to master's in computer science after my graduation in China. I always think I am a very goal-oriented person so to achieve that I can finally land a job in the United States. Also, I am very capable in doing all the challenging work, so that I can handle all of it on my own and lead the team to build for a new goal. And also, I was named as a rock star of the organization last year. And also, my annual review is exceptional, which is the top 5% in our team and our organization. So I think I've already proved that I have the ability and talent to build amazing infrastructure and customer-facing product. But the thing is, I want to do something more. I don't want to be constrained in a single area, but I want to focus more on the infra. and the real product that everyone would like to pay to use. So that is the reason why I'm interested in Snowflake. And as you can see, my daily day-to-day work involves a lot of the Snowflake and I hope that I can get really involved into the development of this great product.

### 19 · me · 26:09–26:26 · 16.8 s · 32 words · segs 190–192

My first question is, this is the general software engineer position, and do you have any specific preference over the qualification and quality of the candidates, and if so, what they are?

### 20 · me · 27:14–28:14 · 59.5 s · 88 words · segs 194–199

Yeah, sure. And given that you are an AI interviewer, so I'm pretty interested in your feedback on me, if that is okay to stay out. Okay, okay, okay, then forget about it. Then I also have another question, which is the following steps on this interview. So, So what is your expectation about this position and what you expect from me? I mean, other than the normal answers, like what is the thing that you value most from an engineer that has already worked from another company?

### 21 · me · 28:56–29:01 · 4.9 s · 14 words · segs 201–201

I think that's it, thank you so much for your help and your tokens.

### 22 · me · 29:15–29:17 · 2.4 s · 4 words · segs 202–203

Yeah, sure. See you.

### 23 · me · 29:34–29:35 · 1.4 s · 3 words · segs 204–204

Yeah, bye bye.
