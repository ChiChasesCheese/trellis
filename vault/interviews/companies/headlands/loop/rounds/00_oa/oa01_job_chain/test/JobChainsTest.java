import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class JobChainsTest {

    private static List<String> lines(String block) { return block.lines().toList(); }

    // ---------- Part 1: parse + hhmmss ----------

    @Test @Tag("part1")
    void parsesHeaderBlankLinesAndSpaces() {
        var jobs = JobChains.parse(lines("""
                #job_id,runtime_in_seconds,next_job_id
                1, 60, 23

                23 ,30,0
                """));
        assertEquals(List.of(new JobChains.Job(1, 60, 23), new JobChains.Job(23, 30, 0)), jobs);
    }

    @ParameterizedTest @Tag("part1") @Tag("edge")
    @ValueSource(strings = {"1,2", "1,2,3,4", "a,2,3", "1;2;3", "0,5,0", "-1,5,0", "3,-5,0", "3,5,-1", "4,1,4",
            "99999999999,1,0"})
    void rejectsBadLines(String bad) {
        assertThrows(JobChains.MalformedInputException.class, () -> JobChains.parse(List.of("#h", bad)));
    }

    @Test @Tag("part1") @Tag("fmt")
    void formatsDurations() {
        assertEquals("00:00:00", JobChains.hhmmss(0));
        assertEquals("00:00:59", JobChains.hhmmss(59));
        assertEquals("00:01:00", JobChains.hhmmss(60));
        assertEquals("01:01:01", JobChains.hhmmss(3661));
        assertEquals("02:00:00", JobChains.hhmmss(7200)); // 常见错误：分钟忘了 % 60 → 02:120:00
        assertEquals("100:00:00", JobChains.hhmmss(360_000));
    }

    // ---------- Part 2: chains ----------

    @Test @Tag("part2")
    void buildsChainsSortedByRuntimeDesc() {
        var chains = JobChains.chains(JobChains.parse(lines("""
                #job_id,runtime_in_seconds,next_job_id
                1,60,23
                23,30,3
                3,15,0
                5,200,0
                """)));
        assertEquals(List.of(new JobChains.Chain(5, 5, 1, 200), new JobChains.Chain(1, 3, 3, 105)), chains);
        assertEquals(35, chains.get(1).averageSeconds());
    }

    @Test @Tag("part2") @Tag("edge")
    void inputOrderDoesNotMatter() {
        var rows = new ArrayList<>(List.of("3,15,0", "1,60,23", "23,30,3"));
        Collections.reverse(rows);
        assertEquals(List.of(new JobChains.Chain(1, 3, 3, 105)), JobChains.chains(JobChains.parse(rows)));
    }

    @Test @Tag("part2") @Tag("edge")
    void tieBreaksOnStartJob() {
        var chains = JobChains.chains(JobChains.parse(List.of("9,10,0", "4,10,0")));
        assertEquals(List.of(4, 9), chains.stream().map(JobChains.Chain::startJob).toList());
    }

    @ParameterizedTest @Tag("part2") @Tag("edge")
    @ValueSource(strings = {
            "1,10,2|2,10,0|1,5,0",        // 重复 id
            "1,10,7",                     // 悬空 next
            "1,10,3|2,10,3|3,10,0",       // 两个前驱（多 parent）
            "1,10,2|2,10,1",              // 纯环，没有链头
            "1,10,0|2,10,3|3,10,2",       // 一条好链 + 一个环
    })
    void rejectsStructuralErrors(String rows) {
        var jobs = JobChains.parse(List.of(rows.split("\\|")));
        assertThrows(JobChains.MalformedInputException.class, () -> JobChains.chains(jobs));
    }

    @Test @Tag("part2") @Tag("edge")
    void emptyInputHasNoChains() {
        assertEquals(List.of(), JobChains.chains(JobChains.parse(List.of("#job_id,runtime_in_seconds,next_job_id"))));
    }

    @Test @Tag("part2") @Tag("edge")
    void hugeRuntimesDoNotOverflowInt() {
        var c = JobChains.chains(JobChains.parse(List.of("1,2000000000,2", "2,2000000000,0"))).getFirst();
        assertEquals(4_000_000_000L, c.totalSeconds());
    }

    // ---------- Part 3: full report ----------

    @Test @Tag("part3") @Tag("fmt")
    void rendersReportExactly() {
        var out = JobChains.solve(lines("""
                #job_id,runtime_in_seconds,next_job_id
                1,60,23
                23,30,3
                3,15,0
                5,200,0
                """));
        assertEquals(lines("""
                -
                start_job: 5
                last_job: 5
                number_of_jobs: 1
                job_chain_runtime: 00:03:20
                average_job_time: 00:03:20
                -
                start_job: 1
                last_job: 3
                number_of_jobs: 3
                job_chain_runtime: 00:01:45
                average_job_time: 00:00:35
                -
                """), out);
    }

    @Test @Tag("part3") @Tag("fmt")
    void officialHackerRankExample() {
        // 原题样例（Chi 截图逐字抄录，mock_maven/catalog/raw/hackerrank_job_runner_photos.md）
        var out = JobChains.solve(lines("""
                #job_id,runtime_in_seconds,next_job_id
                1,60,23
                2,23,3
                3,12,0
                23,30,0
                """));
        assertEquals(lines("""
                -
                start_job: 1
                last_job: 23
                number_of_jobs: 2
                job_chain_runtime: 00:01:30
                average_job_time: 00:00:45
                -
                start_job: 2
                last_job: 3
                number_of_jobs: 2
                job_chain_runtime: 00:00:35
                average_job_time: 00:00:17
                -
                """), out);
    }

    @Test @Tag("part3") @Tag("fmt")
    void malformedIsASingleLine() {
        var outcome = JobChains.analyze(List.of("#h", "1,10,2"));
        assertInstanceOf(JobChains.Malformed.class, outcome);
        assertEquals(List.of("Malformed Input"), JobChains.render(outcome));
    }

    @Test @Tag("part3") @Tag("perf")
    void millionJobsInUnderTwoSeconds() {
        var rnd = new Random(0);
        int n = 1_000_000;
        var ids = new ArrayList<Integer>(n);
        for (int i = 1; i <= n; i++) ids.add(i);
        Collections.shuffle(ids, rnd);
        var rows = new ArrayList<String>(n + 1);
        rows.add("#job_id,runtime_in_seconds,next_job_id");
        for (int i = 0; i < n; i++) {
            boolean tail = i == n - 1 || rnd.nextInt(100) == 0; // 平均每条链 100 个 job
            rows.add(ids.get(i) + "," + rnd.nextInt(3600) + "," + (tail ? 0 : ids.get(i + 1)));
        }
        Collections.shuffle(rows.subList(1, rows.size()), rnd);
        var out = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> JobChains.solve(rows));
        assertEquals("-", out.getFirst());
    }
}
