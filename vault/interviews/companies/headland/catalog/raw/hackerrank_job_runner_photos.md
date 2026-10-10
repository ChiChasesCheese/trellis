# Raw: "Job Runner" — phone photos of a HackerRank screen (Headland)

- **Source:** 3 phone photos supplied by Chi on 2026-10-10 (statement in two parts + the editor template). Not
  committed. Chi describes it as a HackerRank practice attempt, closed before we worked on it here.
- **Company:** Headland per Chi; widely reported elsewhere as a Headland Technologies OA question.
- **Confidence:** statement, example and error rule **high** (read off the screen). Everything the statement leaves
  open is decided in `../../study/q02_job_runner.md` §1 and labelled **(inferred)**.

## Verbatim statement

> **Job Runner**
>
> You work on a highly sophisticated distributed computing platform. Each day it generates a daily log of the jobs
> run. Each job has three properties: a unique integer id, the time it took to run in seconds, and the id of the job
> that ran after it. We call a sequence of jobs a *chain*, and if a job represents the end of the *chain*, its next id
> will be 0. Given the daily log, generate a report summarizing the *chains* run during the day. If the input is
> malformed in any way then an error should be reported.
>
> **Input Format** — Input is provided in CSV format via **STDIN**. The first line is a header, and each subsequent
> line provides the properties for a given job.
>
> ```
> #job_id,runtime_in_seconds,next_job_id
> 1,60,23
> 2,23,3
> 3,12,0
> 23,30,0
> ```
>
> **Output Format** — The resulting summary report should be emitted via **STDOUT**. Each section in the report
> describes a *chain*, and the sections should be in descending order based on the total runtime of the chain.
>
> ```
> -
> start_job: id of the first job in the chain
> last_job: id of the last job in the chain
> number_of_jobs: number of jobs in the chain
> job_chain_runtime: total runtime of the chain in HH:MM:SS
> average_job_time: average per-job runtime in HH:MM:SS
> -
> start_job: id of the first job in the chain
> last_job: id of the last job in the chain
> number_of_jobs: number of jobs in the chain
> job_chain_runtime: total runtime of the chain in HH:MM:SS
> average_job_time: average per-job runtime in HH:MM:SS
> -
> ```
>
> Given the example input above, the summary report would look like:
>
> ```
> -
> start_job: 1
> last_job: 23
> number_of_jobs: 2
> job_chain_runtime: 00:01:30
> average_job_time: 00:00:45
> -
> start_job: 2
> last_job: 3
> number_of_jobs: 2
> job_chain_runtime: 00:00:35
> average_job_time: 00:00:17
> -
> ```
>
> If the input is malformed in any way - for example:
>
> ```
> garbage
> ```
>
> Then your program should exit zero and print the following error message to **STDOUT**:
>
> ```
> Malformed Input
> ```
>
> **Note** — The examples we provide aren't exhaustive, so be sure to test your code thoroughly. A human will review
> the code as well.

## Editor template (Java) as shown

```java
import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {
    public static void main(String args[]) throws Exception {
        /* Enter your code here. Read input from STDIN. Print output to STDOUT */
    }
}
```

## What the example pins down

- Average is **truncated**, not rounded: chain 2→3 is 35 s over 2 jobs = 17.5 → `00:00:17`.
- The report opens with `-` and every section ends with `-`.
- Line order in the file is not chain order: job 23 is listed last but belongs to the first chain.
