# Glassdoor 全量工程面经（Abnormal AI，company id 3146005）· 抓取 2026-10-09

访问日期 2026-10-09；可信度 [中]（匿名单条评论，无法核实；Glassdoor 评论日期 = 发布日期，"interviewed" = 评论者自填的面试月份）。
抓取方式：`curl` + 浏览器 UA，直接 200（与 `AGENT_RESEARCH.md` 里"glassdoor 403"不同，api.glassdoor.com 域名 + 浏览器 UA 可达）。页面把评论放在内嵌 JSON（`"interviews":[...]`，每页 5 条）；解析脚本与原始 HTML 在 `$CLAUDE_JOB_DIR/tmp/glassdoor/`（`parse.py` / `reviews.json`，不入库）。
覆盖：公司全部面经列表 `https://api.glassdoor.com/Interview/Abnormal-AI-Interview-Questions-E3146005.htm`（`_P2`…`_P31`）共 152 条（站点自报 `filteredInterviewCount` = 152，全部取到）；其中工程相关 78 条（见下表）。非工程（销售、CS、安全分析师、PM 等）不收。
分角色页（含页内重复）：Software Engineer 26（页面自称 28，另含 2 条标题为 Software Developer）· Senior Software Engineer 14 · Software Engineer II 9 · Machine Learning Engineer 3 · 其余工程标题（Backend Engineer、SDE-2 变体、Full Stack、Director of Engineering、Senior Engineering Manager、DevOps、Data Scientist、Engineering Intern、"Interviewee"）散在全量列表。
URL 形态：单条评论 `https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW<id>.htm`；角色页 `…Abnormal-AI-Software-Engineer-Interview-Questions-EI_IE3146005.0,11_KO12,29[_IP2…].htm`，Senior = `KO12,36`，SWE II = `KO12,32`（kit 旧文写 `KO12,31`，该 URL 的角色 slug 是 "Software-Engineer-2"），MLE = `KO12,37`。

数量：工程评论 78 条；已在 kit 的 11 条；新增 67 条（其中提到 AI / take-home / code review / 系统设计 / incident / 具体题的见 §2）。
"已收"判定：按日期 + 标题 + 原文片段与 `process_and_rounds.md` / `questions_reported.md` / `ai_round_sweep_2026-10-07.md` 比对；仅"同一来源另有别的候选人讲过类似内容"不算已收。

## 1. 全部工程评论

| 评论日期 | 面试月 | review id | 标题 | 地点 | 结果 | 轮次结构（≤15 词） | AI/take-home/Claude/Cursor |
|---|---|---|---|---|---|---|---|

| 2026-10-08 | - | 105890472 | Software Engineer | United States | No offer | HR talk (project dive+BQ); AI coding on provided codebase; technical deep dive | AI |
| 2026-07-15 | - | 104796646 | SWE 2 | New York, NY | No offer | HM interview; then technical screen | - |
| 2026-07-15 | - | 104787687 | Sde 2 | Bengaluru | No offer | AI coding: big codebase understood via AI; implement feature+tests (Sentinal, rule engine) | AI |
| 2026-07-10 | - | 104734189 | Senior Software Engineer | Bengaluru | No offer | HM round; asked how I use AI day to day 已收 | AI |
| 2026-07-07 | 2026-06 | 104679337 | Software Engineer II | Bengaluru | No offer | Recruiter; Round 1 (10 days later) Claude Code feature in large codebase; explain | AI/Claude |
| 2026-06-29 | - | 104578961 | Senior Software Engineer | United States | Accepted | Recruiter, HM, tech round, virtual onsite (3 technical) 已收 | - |
| 2026-06-16 | 2026-04 | 104417664 | Software Engineer II | United States | No offer | Take-home file-upload dedup+search; review round: explain, add content search | AI/take-home |
| 2026-06-10 | 2026-04 | 104329591 | Software Engineer II | United States | Accepted | Recruiter, HM, tech round, virtual onsite; AI tools allowed; incident on-call scenario | AI |
| 2026-06-03 | - | 104243539 | Software Engineer II | Bengaluru | No offer | 24h take-home file storage vault; AI allowed (self-paid); record video of AI use | AI/take-home |
| 2026-06-03 | 2026-05 | 104234672 | Senior Software Engineer | United States | No offer | Recruiter, manager screen, AI-assistant coding, take-home code review 已收 | AI/take-home |
| 2026-05-05 | - | 103828771 | Software Engineer | Singapore | No offer | Take-home application; evaluated on how you prompt AI 已收 | AI/take-home |
| 2026-04-17 | 2026-04 | 103602500 | Software Engineer II | United States | No offer | AI coding round with Cursor; interviewer nudged to keep speaking; rejected | AI/Cursor |
| 2026-04-16 | 2026-02 | 103595979 | Software Engineer | Singapore | Accepted | Take-home; assignment review; SD+incident; code review+fix with AI; EM 已收 | AI/take-home |
| 2026-04-08 | 2026-03 | 103476901 | SDE-2 | India | No offer | Take-home; assignment round; incident mgmt+HLD; PR review; AI allowed in all | AI/take-home |
| 2026-04-05 | - | 103435482 | Software Engineer | New York, NY | Declined offer | Phone screen; loop: HM, system design, past project; AI/lookup allowed | AI |
| 2026-03-27 | 2026-03 | 103339969 | Software Engineer | United States | Accepted | Recruiter, rounds with instructions; incident management on-call simulation | - |
| 2026-03-22 | 2026-02 | 103260492 | Senior Software Engineer | London, England | No offer | Told Cursor/no leetcode; interviewer asked duplicate-finding in browser Python IDE | AI/Cursor |
| 2026-03-12 | - | 103142802 | Software Engineer | South Korea | No offer | Take-home (8h+), then screening call; rejected in 5 min 已收 | take-home |
| 2026-02-25 | 2026-02 | 102948019 | Software Development Engineer (SDE) | Sunnyvale, CA | No offer | Recruiter screen; coding in Cursor IDE assessed by AI | AI/Cursor |
| 2026-02-23 | 2026-01 | 102917399 | Software Engineer | San Francisco, CA | Accepted | Referral; recruiter, HM (ownership); about a month 已收 | - |
| 2026-02-10 | 2026-01 | 102779298 | Software Engineer II | United States | No offer | Nine rounds; incident handling with AWS; system design whiteboard | - |
| 2026-01-27 | - | 102506999 | Engineering Intern | Canada | No offer | Intern: first round BQ, 30 min | - |
| 2026-01-08 | 2025-12 | 102142539 | Interviewee | Chicago, IL | No offer | Negative; no process detail | - |
| 2025-12-03 | 2025-11 | 101613002 | Software Engineer II | Bengaluru | No offer | Take-home; recruiter call; interview on assignment: design, 10x scale, follow-up feature | take-home |
| 2025-11-04 | 2025-06 | 101070673 | Software Developer | Bengaluru | Declined offer | Recruiter complaints; panel good | - |
| 2025-11-04 | - | 101069333 | Senior Software Engineer | India | Declined offer | Recruiter; take-home; technical discussion; managerial; salary | take-home |
| 2025-10-17 | 2025-09 | 100709329 | Software Enigneer | Dallas, TX | No offer | Phone screen; take-home; technical debrief; asked how you use AI | AI/take-home |
| 2025-09-19 | 2025-08 | 100112992 | Software Engineer - Full Stack - 1 | Bengaluru | Accepted | AI-driven app build; app extension round; two HM rounds; HR | AI |
| 2025-09-16 | 2024-09 | 100030096 | Software Engineer | India | No offer | Online coding; take-home discussed; past-work round (JSON Schema parsing) 已收 | take-home |
| 2025-08-01 | 2025-03 | 99099286 | Senior Software Engineer | London, England | No offer | Passed all stages; verbal offer then withdrawn 已收 | - |
| 2025-07-22 | - | 98873551 | Senior Software Engineer | United States | No offer | Recruiter cancelled 5 min before call (Bay Area hiring) | - |
| 2025-07-18 | 2025-06 | 98785055 | Software Engineer II SDE2 | India | Declined offer | Take-home; debrief; extra round after clearing five | take-home |
| 2025-06-23 | 2025-06 | 98208370 | Software Developer | Bengaluru | No offer | Django take-home with Cursor/ChatGPT + video; live extension with AI; HM | AI/take-home/Cursor |
| 2025-06-09 | - | 97915489 | Seniot | India | No offer | Django file-sharing take-home (2h); no recruiter contact | take-home |
| 2025-06-04 | - | 97826423 | Software Engineer | Canada | No offer | Recruiter; 1h technical, 15 min LC-style hashing; HM | - |
| 2025-06-03 | 2025-05 | 97779682 | Full Stack Software Engineer | United States | Accepted | Tech phone screen; HM; onsite: project, system design, frontend, code review | - |
| 2025-05-20 | - | 97482615 | Software Engineer | Singapore | No offer | Take-home for hours; recruiter call ended in 5 min | take-home |
| 2025-05-15 | 2025-02 | 97378354 | Software Engineer | Canada | No offer | Code review prompt: feedback if written by a junior | - |
| 2025-05-09 | 2025-05 | 97238937 | Software Engineer II | Bengaluru | No offer | Take-home: React+Django on boilerplate, using AI tools | AI/take-home |
| 2025-04-15 | - | 96701245 | Software Engineer | Germany | No offer | Recruiter call with bot recording | - |
| 2025-03-06 | - | 95576460 | Software Engineer | Singapore | No offer | Easy Python OOP OA, then ghosted | - |
| 2025-03-02 | 2025-01 | 95471882 | Director of Engineering | London, England | Accepted | Director of Engineering: leadership loop | - |
| 2025-02-08 | - | 94885533 | Software Engineer | San Francisco, CA | Accepted | Technical interview with HM; resume deep dive | - |
| 2025-02-04 | - | 94788910 | Backend Engineer | Singapore | No offer | HR; OA; technical screen: 'you code I watch' for an hour | - |
| 2024-11-08 | 2024-09 | 92668268 | SDE 2 Software Engineer | Bengaluru | No offer | Phone; HM; 2 technical (JSON, component design, Python debug); SD | - |
| 2024-11-02 | - | 92489809 | Software Engineer | United States | No offer | Recruiter call; rejection | - |
| 2024-10-15 | - | 91953144 | Backend Engineer | United States | No offer | HR; technical 45 min LC medium (two interviewers) | - |
| 2024-09-12 | - | 90934008 | Senior Software Engineer | Toronto, ON | No offer | Recruiter; HM phone 已收 | - |
| 2024-09-03 | - | 90672648 | Senior Machine Learning Engineer | United Kingdom | No offer | Senior MLE: NDA | - |
| 2024-08-02 | - | 89713778 | Backend Software Engineer | United States | No offer | Codility offered, then ghosted | - |
| 2024-07-26 | 2024-07 | 89534331 | Software Engineer II | Canada | No offer | HR, HM, live coding 1h (2 LC), panel, behavior | - |
| 2024-07-26 | 2024-07 | 89513117 | Senior Full Stack Engineer | India | No offer | HR; HM; no feedback | - |
| 2024-07-04 | - | 88851198 | Machine Learning Engineer | San Francisco, CA | No offer | MLE: LC medium variants | - |
| 2024-06-22 | 2024-05 | 88492309 | Senior Software Engineer | Toronto, ON | No offer | Photo de-duplication pipeline design | - |
| 2024-06-12 | 2023-06 | 88192157 | Software Engineer 2 | India | No offer | Python OA (real-world, not DSA); closed 已收 | - |
| 2024-05-18 | - | 87405358 | Senior Software Engineer | United Kingdom | No offer | Salary band dispute; rejected | - |
| 2024-05-11 | 2024-02 | 87170873 | Software Engineer | Singapore | No offer | First round: optimise a game; unclear question | - |
| 2024-05-10 | - | 87159919 | Software Engineer | United States | No offer | HR, HM, technical screen: hashing/photo use case | - |
| 2024-05-03 | 2024-04 | 86941145 | Senior Software Engineer | San Francisco, CA | No offer | 'Know Python inside and out' | - |
| 2024-04-25 | 2024-04 | 86675817 | Senior Machine Learning Engineer | Canada | No offer | Senior MLE: relevant experience | - |
| 2024-04-22 | 2024-04 | 86559516 | Software Engineer | United States | No offer | Recruiter; 60 min: discussion, live coding, questions (hashing) | - |
| 2024-04-08 | 2024-01 | 86106362 | Software Engineer | Canada | No offer | HR, HM, tech screen (hashing), panel, behavior | - |
| 2024-01-24 | 2023-11 | 83662804 | Senior Engineering Manager | Canada | No offer | Sr Eng Manager: phone screen only | - |
| 2023-12-16 | - | 82642279 | Software Engineer | Singapore | No offer | Vague directions; toxic interviewers | - |
| 2023-11-02 | - | 81473501 | Backend Developer 2 | Bengaluru | No offer | CodeSignal; HR; HM sorting question | - |
| 2023-10-20 | - | 81112823 | Senior Software Engineer | Singapore | No offer | Recruiter no-show | - |
| 2023-06-15 | - | 77393167 | Senior Software Engineer | Bengaluru | No offer | Python-focused unique questions; NDA | - |
| 2023-05-14 | 2023-05 | 76407933 | Software Engineer | Bengaluru | Accepted | Python script (JSON parse/validate); site manager; 2 tech; offer | - |
| 2023-04-30 | - | 75976956 | Machine Learning Engineer | New York, NY | No offer | MLE: ML fundamentals, design, spam features | - |
| 2023-04-04 | - | 75190801 | Software Engineer | United States | No offer | Two developers; Python easy; syntax-focused | - |
| 2022-07-31 | 2022-03 | 67356720 | Data Scientist | Poland | No offer | Data Scientist: standard data analysis | - |
| 2022-07-21 | 2022-07 | 66956361 | Machine Learning Engineer | San Francisco, CA | No offer | MLE: recruiter; 1h coding challenge | - |
| 2022-05-11 | - | 63983183 | Devops Engineer | United States | No offer | DevOps: HM; 30 min projects + CSV session-time coding | - |
| 2022-02-25 | - | 60270881 | Senior Software Engineer | Canada | No offer | Phone screen: string manipulation; design patterns | - |
| 2021-11-22 | 2021-11 | 55674540 | Software Engineer | United States | No offer | Recruiter, 2 phones, 4 virtual onsites; project dives | - |
| 2021-02-25 | - | 43105318 | Software Engineer | Seattle, WA | Accepted | Chat with VP; phone; 4-interview final; skeleton code, SD, deep dive | - |
| 2021-01-24 | - | 41315964 | Software Engineer | United States | No offer | Optimise a solution; MapReduce+LC style (hangman) | - |
| 2021-01-14 | - | 40671720 | Software Engineer | United States | No offer | AngelList; Director chat; DS/A phone; session-time log | - |

## 2. 新增评论原文（逐条，英文原句不改）

### 105890472 · 2026-10-08 · Software Engineer · United States · NO_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW105890472.htm · 访问 2026-10-09 · [中]

> first round HR talk, mostly project deep dive and BQ 
> second rd ai coding, use an provided codebase
> third round technical deep dive
> not sure if there will be more rounds

### 104787687 · 2026-07-15 · Sde 2 · Bengaluru · NO_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW104787687.htm · 访问 2026-10-09 · [中]

> Ai coding.
> Was given a big codebase and was asked to understand the codebase using Ai.
> And then I was asked to implement a feature using Ai and write tests for the same
> 
> Q: was given Sentinal code base - asked to implement a rule engine

### 104679337 · 2026-07-07 · Software Engineer II · Bengaluru · NO_OFFER · interviewed 2026-06
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW104679337.htm · 访问 2026-10-09 · [中]

> Round 0: Recruiter screen where we discussed about what Abnormal does and what the interview process is going to look like. This was followed by Round 1 scheduled after 10 days, it was an AI assisted coding interview where given a large codebase and a feature requirement, you need to implement that feature by prompting claude code.
> 
> Q: Explain the architecture of the codebase, explain the feature which I have added and how will you make sure it works

### 104417664 · 2026-06-16 · Software Engineer II · United States · NO_OFFER · interviewed 2026-04
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW104417664.htm · 访问 2026-10-09 · [中]

> The interview process was quite extensive.  It began with a take-home assignment to build a file-upload application with deduplication and search functionality, which I completed and submitted. They was accepted my solution and passed me along to review round. This is where I was rejected. They asked me to describe my architectural decision and how I used AI in my design and development. The guy was impressed and then he asked me to add a feature in the take home to be able to search the content of the file? I mentioned the solution due to spending too much time in dicussion. I didn't have enough time to implement it.
> 
> Q: Take Home: File App (Search by filename and Dedupe)
> 
> Take Home review: Explain your design. Implement add on feature to search the file by its content.

### 104329591 · 2026-06-10 · Software Engineer II · United States · ACCEPT_OFFER · interviewed 2026-04
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW104329591.htm · 访问 2026-10-09 · [中]

> Process was recruiter call, hiring manager screen, tech round, and virtual onsite. Hiring manager asked about previous experiences and what you learned from them. Was able to use AI tools for tech rounds and virtual onsite which was helpful. Interviewers were responsive and accommodating throughout should you have scheduling conflicts
> 
> Q: Incident handling for on call type scenario

### 104243539 · 2026-06-03 · Software Engineer II · Bengaluru · NO_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW104243539.htm · 访问 2026-10-09 · [中]

> I was given a take-home assignment with a completion time of 24 hrs. It was about building a file storage vault. AI tools were allowed, but they did not provide any. I had to buy my own. 
> 
> Expectation was also there to record a video on how I used AI tools to develop the task.
> They rejected me without giving any feedback. Very bad experience
> 
> Q: Build a file storage vault with AI tools.

### 103602500 · 2026-04-17 · Software Engineer II · United States · NO_OFFER · interviewed 2026-04
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW103602500.htm · 访问 2026-10-09 · [中]

> Wasted my time interviewing here; the AI coding round is stupid.
> The interviewer was constantly nudging me to keep speaking. It was so hard to understand how they want me to use an AI agent to code that relatively easy problem. I was constantly fighting with the auto-complete of cursor and couldn't focus on the problem.  I would rather have done it without the AI constantly trying to erase my implementation.
> 
> Absolute waste of time and my confidence. Nothing but template rejection at the end.

### 103476901 · 2026-04-08 · SDE-2 · India · NO_OFFER · interviewed 2026-03
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW103476901.htm · 访问 2026-10-09 · [中]

> 4 rounds with initial first round take home assignment, 2nd round will be based on assignment, 3 round will be incident management and HLD, 4th Round is PR review , you can use AI agents in all the rounds.

### 103435482 · 2026-04-05 · Software Engineer · New York, NY · DECLINE_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW103435482.htm · 访问 2026-10-09 · [中]

> Practical problems that were different than your typical leetcode style questions. They let you look stuff up and use AI if you need it. Interview consisted of phone screen, and then full loop with hiring manager, system design, past project review.

### 103339969 · 2026-03-27 · Software Engineer · United States · ACCEPT_OFFER · interviewed 2026-03
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW103339969.htm · 访问 2026-10-09 · [中]

> The interview process was well organized and recruiter explained each step clearly. There were detailed instructions for each round that matched up with what interviewers expected. Things progressed quickly and smoothly between rounds, and recruiters were easy to communicate with.
> 
> Q: Incident management - simulation of an on call scenario

### 103260492 · 2026-03-22 · Senior Software Engineer · London, England · NO_OFFER · interviewed 2026-02
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW103260492.htm · 访问 2026-10-09 · [中]

> I was told to expecton backend programming topics and no leetcode style questions and expect to use Cursor. Person who interviewed with me was from a different team and they asked me a leet code question on a browser based phyton ide . If I was given correct information I would have study on algorithm questions.
> 
> Q: A question on finding duplicates

### 102948019 · 2026-02-25 · Software Development Engineer (SDE) · Sunnyvale, CA · NO_OFFER · interviewed 2026-02
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW102948019.htm · 访问 2026-10-09 · [中]

> Round 1: Recruiter Screening
> Round 2: Coding using cursor ide assessment
> They use AI to assess the code. It checks for green flags   
> Round 1: Recruiter Screening
> Round 2: Coding using cursor ide assessment
> They use AI to assess the code. It checks for green flags   
> Round 1: Recruiter Screening
> Round 2: Coding using cursor ide assessment
> They use AI to assess the code. It checks for green flags
> 
> Q: Round 1: Recruiter Screening
> Round 2: Coding using cursor ide assessment
> They use AI to assess the code. It checks for green flags

### 102779298 · 2026-02-10 · Software Engineer II · United States · NO_OFFER · interviewed 2026-01
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW102779298.htm · 访问 2026-10-09 · [中]

> The interview process is LONG. 9 rounds of interviews, and they are very good at making you feel confident until the very end. If one person on the interview committee doesn’t like you, you will not get the role. Even if you make a great impression on 8/9, one hiccup and you’re out. Some interviewers are very prideful, and if you don’t say exactly what they are thinking, they will not proceed.
> 
> Q: Incident handling with AWS and system design whiteboard question

### 102142539 · 2026-01-08 · Interviewee · Chicago, IL · NO_OFFER · interviewed 2025-12
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW102142539.htm · 访问 2026-10-09 · [中]

> Don't even bother! Very unprofessional and a waste of time. Company needs to figure their stuff out before putting up job posts, there are other bad reviews here for a reason and you should listen to them.
> 
> Q: Why do you want to work here?

### 101613002 · 2025-12-03 · Software Engineer II · Bengaluru · NO_OFFER · interviewed 2025-11
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW101613002.htm · 访问 2026-10-09 · [中]

> I applied through their portal, received a take-home assignment, submitted it, and then had a recruiter screening call about my experience before I got the interview. The interview was based on the assignment and included a follow-up feature discussion.
> 
> Q: Discussion on the design choices I made for the assignment, how I would scale it for 10x users, and a follow-up feature to implement during the call.

### 101069333 · 2025-11-04 · Senior Software Engineer · India · DECLINE_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW101069333.htm · 访问 2026-10-09 · [中]

> The interview process includes recruiter screening, multiple technical rounds covering coding, system design, and architecture, followed by behavioral and leadership interviews, assessing technical expertise, problem-solving ability, communication, and cultural alignment before final offer.
> 
> Q: Take home assignment
> technical discussion
> Mangerial
> Salary

### 100709329 · 2025-10-17 · Software Enigneer · Dallas, TX · NO_OFFER · interviewed 2025-09
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW100709329.htm · 访问 2026-10-09 · [中]

> Had a phone screen where I was asked about my qualifications and then given a take home challenge (which requires a lot of time and effort). After that I was invited for a technical debrief. Recruiter was very quick to get back to me with any questions I had and the technical debrief was very thorough.
> 
> Q: How do you use AI?

### 100112992 · 2025-09-19 · Software Engineer - Full Stack - 1 · Bengaluru · ACCEPT_OFFER · interviewed 2025-08
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW100112992.htm · 访问 2026-10-09 · [中]

> The process included creating and extending an AI-driven end-to-end application, an app extension round, followed by two hiring-manager rounds and one HR round evaluating technical depth, scalability, usability, and AI integration skills.
> 
> Q: Resume Discussion and Projects discussion.

### 98785055 · 2025-07-18 · Software Engineer II SDE2 · India · DECLINE_OFFER · interviewed 2025-06
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW98785055.htm · 访问 2026-10-09 · [中]

> Cleared all the rounds and then 1 week no response and after that they call and tell they want to schedule one more round to be 100 % sure that i can solve their real life problems or not. if they cant judge me in 5 rounds then it is my mistake or their,  why they need one more round to do so. the interviewer seems to in experienced, The HR neither gave the feedback nor took the feedback, they believe they are the best
> 
> Q: take home assignment, debrief on the solution and other rounds

### 98208370 · 2025-06-23 · Software Developer · Bengaluru · NO_OFFER · interviewed 2025-06
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW98208370.htm · 访问 2026-10-09 · [中]

> The process had 3 stages, firstly a take home assignment based on Django in which we were specifically asked to use Cursor/ChatGPT(or any other). We were also required to record a video along with this on how we used AI to speed up the process. Second round was an extension of this. It was a live coding round in which the interviewer first asked me to explain the flow and then gave me an extended version of the same problem to code using  AI. Third round was Hiring Manager round which was a cultural fit round.
> 
> After this they told me the feedback was positive but then they started ghosting me when I asked them when can I expect the offer letter.
> The HRs doesn't have any basic courtesy to atleast reply to a single mail/call.
> 
> Q: Normal cultural fit questions based on their VOICE framework

### 97915489 · 2025-06-09 · Seniot · India · NO_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW97915489.htm · 访问 2026-10-09 · [中]

> Was given an assignment, no recruiter contacted but was given a test to build some capabilities for file sharing Django project.
> 
> It was very easy, completed in 2 hours. Later got system generated email, recruiters do not even have basic courtesy to call and provide feedback.
> 
> DO NOT WASTE YOUR TIME!
> 
> Q: take home test to add some capabilities for file sharing Django project.

### 97779682 · 2025-06-03 · Full Stack Software Engineer · United States · ACCEPT_OFFER · interviewed 2025-05
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW97779682.htm · 访问 2026-10-09 · [中]

> I had a negative experience interviewing with Abnormal. I received an offer (compensation in a tool via Pave which is essentially a verbal offer). Unfortunately, during the negotiation process, my offer was rescinded because they decided to go with another candidate. Do not negotiate with this company unless you have a written offer!
> 
> The process itself was: Technical phone screen (coding), then hiring manager behavioral screen, then onsite - past project review, system design, frontend interview, and a code review interview.
> 
> Q: Standard coding, system design, behavioral questions

### 97482615 · 2025-05-20 · Software Engineer · Singapore · NO_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW97482615.htm · 访问 2026-10-09 · [中]

> I had a disappointing experience with this company's recruitment process. After spending several hours completing a take-home assignment they provided, I was scheduled for a recruiter call. However, the recruiter ended the call within five minutes after realizing I had applied about a year ago.
> 
> It was clear they hadn’t properly reviewed my background before assigning the take-home task, which wasted a significant amount of my time. I followed up via email but received no personal response—just an automated rejection. There was no acknowledgment or apology for the time I spent.
> 
> This experience reflects a lack of consideration for candidates’ time and suggests inefficiencies in their recruitment screening process.
> 
> Q: Interview ended in five minutes

### 97238937 · 2025-05-09 · Software Engineer II · Bengaluru · NO_OFFER · interviewed 2025-05
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW97238937.htm · 访问 2026-10-09 · [中]

> $50
> 
> Q: They asked me to complete a take-home assignment involving full-stack development (React.js for frontend and Django for backend), using AI tools to implement the features outlined in the provided boilerplate project.

### 92668268 · 2024-11-08 · SDE 2 Software Engineer · Bengaluru · NO_OFFER · interviewed 2024-09
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW92668268.htm · 访问 2026-10-09 · [中]

> Phone call > Hiring manager > 2 technical round > System design round on one end to end system that you have worked on
> 
> I went through the whole process took 2 months but after last interview HR ghosted, wouldn't recommend.
> 
> Q: Json parsing (easy), frontend component design, backend debugging (python debugging) and problem solving

### 88492309 · 2024-06-22 · Senior Software Engineer · Toronto, ON · NO_OFFER · interviewed 2024-05
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW88492309.htm · 访问 2026-10-09 · [中]

> $50
> 
> Q: Design a photo de-duplication pipeline

### 43105318 · 2021-02-25 · Software Engineer · Seattle, WA · ACCEPT_OFFER
https://www.glassdoor.com/Interview/Abnormal-AI-Interview-E3146005-RVW43105318.htm · 访问 2026-10-09 · [中]

> Set up initial chat with VP which was very informative, and he spent a lot of time addressing my concerns and how Abnormal could be a fit for what I was looking for. There was one phone screen and a final round which had four interviews. 
> 
> I felt the questions were fair and tested my abilities to communicate, debug, and design., not just how well I could leetcode. The interviewers were engaging and my past projects deep dive was the most thorough interview I’ve done in my life. There weren’t any leetcode “trick” questions that required some leap of intuition in order to solve.
> 
> Q: Complete skeleton code using data structures and algorithms || System design with focus on databases and data flow || Past projects technical deep dive


## 3. 对 AI Technical Screen 的新信息（只列事实，括号里是 review id 与评论日期）

1. 2026-10-08 最新一条（105890472）：HR 轮（project deep dive + BQ）→ 第二轮 "ai coding, use an provided codebase" → 第三轮 technical deep dive；"not sure if there will be more rounds"。AI 编码轮排在第二轮、技术深挖在其后，与 Chi 的路径（HR + HM → AI screen）同序。
2. Claude Code 明确出现：Round 1 在 recruiter 之后约 10 天，"AI assisted coding interview where given a large codebase and a feature requirement, you need to implement that feature by prompting claude code"；复盘问题 "Explain the architecture of the codebase, explain the feature which I have added and how will you make sure it works"（104679337，2026-07-07，面试 2026-06）。
3. 代码库名字与功能：印度 SDE 2 报告 "was given Sentinal code base - asked to implement a rule engine"，流程是"用 AI 理解大代码库 → 用 AI 实现 feature → 写测试"（104787687，2026-07-15）。这是 kit 以外第二个直接给出代码库名称的来源；注意 kit 自己的 `cb01 t3`/练习库也叫 sentinel，来源是否同一信息需 Chi 自查。
4. Cursor 阶段（更早）：2026-02 面试 "Coding using cursor ide assessment. They use AI to assess the code. It checks for green flags"（102948019，2026-02-25，Sunnyvale）；2026-04 面试者在 AI 轮和 Cursor 自动补全打架："constantly fighting with the auto-complete of cursor"、"The interviewer was constantly nudging me to keep speaking"，不清楚面试官想让 agent 怎么用（103602500，2026-04-17）。→ 讲话/外化思路被主动催促。
5. 评分口径旁证：评审用 AI 查代码里的 "green flags"（102948019）；复盘强调解释架构与"如何确保它能用"（104679337）；含糊但被评价的是 prompt 思路："They want to see your thinking and how you prompt AI"（103828771，take-home）。
6. AI 工具在后续轮次都允许：tech rounds 与 virtual onsite "Was able to use AI tools"（104329591，2026-06-10，Accepted）；"you can use AI agents in all the rounds"（103476901，2026-04-08）；"They let you look stuff up and use AI if you need it"（103435482，2026-04-05）。
7. 并非所有 AI 轮都是干净的：有人被告知"no leetcode style、expect to use Cursor"，实际面试官（别的团队）在浏览器 Python IDE 里出了 "A question on finding duplicates"（103260492，2026-03-22，London）。
8. 后续轮次（新证据）：incident 是 on-call 模拟，"Incident management - simulation of an on call scenario"（103339969，2026-03-27，Accepted）、"Incident handling for on call type scenario"（104329591）、"Incident handling with AWS and system design whiteboard question"（102779298，2026-02-10；"9 rounds of interviews"，"If one person on the interview committee doesn't like you, you will not get the role"）。
9. Take-home 之后的 review 轮会当场加 feature：先"describe my architectural decision and how I used AI"，再"add a feature in the take home to be able to search the content"（104417664，2026-06-16，因讨论占时没做完而被拒）。
10. 阶段数：recruiter → HM → tech（AI）→ virtual onsite（3 个技术轮）约 28–30 天（104578961，Accepted；104329591，28 天）；另有"9 rounds"的长流程（102779298）。
11. HM 轮会问 AI 使用习惯（104734189；100709329 "How do you use AI?"），也有 HM 压 scope、问 "how many lines of code"（104234672，已收）。
12. 小范围 Panel 文化信息：负面评论多集中在 recruiter 沟通（取消、ghosting、offer 撤回 97779682 "my offer was rescinded"），技术面本身评价参差。

### take-home → 现场 AI screen 的时间线（按评论日期 + 面试月）

| 时点 | 证据 | 形态 |
|---|---|---|
| 面试 2024-09（发布 2025-09-16） | 100030096 | 在线编码 + take-home（JSON Schema parsing），旧流程 |
| 评论 2025-05-09 | 97238937 | take-home，React + Django boilerplate，"using AI tools" |
| 面试 2025-06（评论 06-23） | 98208370 | Django take-home，"specifically asked to use Cursor/ChatGPT"，录屏；第二轮现场用 AI 扩展 |
| 评论 2025-06-04 / 06-03 | 97826423 / 97779682 | 仍有旧式 15 分钟 LC 式 hashing 题、phone screen + onsite（含 frontend、code review） |
| 面试 2025-09 ~ 2025-11 | 100709329, 101613002 | take-home → debrief；评审轮"how you would scale it for 10x users" + 现场加 feature |
| 面试 2026-02（评论 02-25） | 102948019 | **首次出现不含 take-home 的现场 Cursor 编码轮**（recruiter → Cursor IDE assessment） |
| 面试 2026-02 ~ 2026-04 | 103595979, 103476901, 104417664, 103602500 | 四轮 take-home 版（Singapore/India/US）与 "AI coding round with Cursor"（US，04）并存 |
| 面试 2026-05（评论 06-03） | 104234672 | recruiter → manager → "coding exercise with AI assistant" → take-home code review |
| 评论 2026-06-03 ~ 06-16 | 104243539, 104417664 | **take-home 仍在发**（24h File Vault，录屏；US 的 file upload + dedup + search） |
| 面试 2026-06（评论 07-07 ~ 07-15） | 104679337, 104787687 | 现场 "AI assisted coding"，明确 **Claude Code**，大代码库（Sentinal，rule engine） |
| 评论 2026-10-08 | 105890472 | 第二轮 "ai coding, use an provided codebase" |

结论：**不是一次干净的切换，而是并行过渡**。take-home 版本从 2025-05 起就已带 AI；现场 AI-in-codebase 轮最早的 Glassdoor 证据是 2026-02（Cursor），Claude Code 明确出现于 2026-06 面试；而 take-home 仍在 2026-06 评论日期出现。按地区看，Singapore/India 报告 take-home 更久，美国 2026-06 之后报告以现场 AI screen 为主，但美国也有 2026-04 面试的 take-home（104417664）。推断（非原文）：大约 2026-02 起现场 AI screen 在美国推广，2026-06 起工具从 Cursor 转 Claude Code。

## 4. 与 kit 已有内容的出入

- `process_and_rounds.md` §0/§3 称"所有渠道均未提及框架（Django/Flask/FastAPI）"：Glassdoor 对 **take-home** 多次明说 Django（98208370, 97915489, 97238937 React+Django）；现场 AI screen 的代码库框架仍无报道（只有 "Sentinal"）。
- "2026 年的报道几乎一致：不是 LeetCode"：103260492（London，2026-02 面试）与 97826423（Canada，2025-06）仍遇到 LC 式 duplicate/hashing 题，且面试官来自别的团队；说明路径因地区/团队而异。
- "Glassdoor 直连 403"（`ai_round_sweep_2026-10-07.md` §渠道表）：用浏览器 UA 的 curl 打 `api.glassdoor.com` 直接 200，可全量取得。
- 若 recruiter 说"expect to use Cursor"，实际工具可能是 Claude Code（2026-06 之后），不要只练一种。
