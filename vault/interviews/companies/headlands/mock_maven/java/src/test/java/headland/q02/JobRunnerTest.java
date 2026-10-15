package headland.q02;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import headland.Impl;
import java.time.Duration;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

class JobRunnerTest {

    private static final String HEADER = "#job_id,runtime_in_seconds,next_job_id\n";
    private static final String MALFORMED = "Malformed Input\n";

    private static String run(String stdin) {
        return Impl.runMain("q02", stdin).replace("\r\n", "\n");
    }

    private static String section(long start, long last, int jobs, String runtime, String average) {
        return """
                start_job: %d
                last_job: %d
                number_of_jobs: %d
                job_chain_runtime: %s
                average_job_time: %s
                -
                """.formatted(start, last, jobs, runtime, average);
    }

    // ---- from the statement -----------------------------------------------------------------------------------

    @Test
    void statementExample() {
        String input = HEADER + """
                1,60,23
                2,23,3
                3,12,0
                23,30,0
                """;
        assertEquals("-\n" + section(1, 23, 2, "00:01:30", "00:00:45") + section(2, 3, 2, "00:00:35", "00:00:17"),
                run(input));
    }

    @Test
    void statementGarbage() {
        assertEquals(MALFORMED, run("garbage\n"));
    }

    // ---- malformed: every case must print exactly "Malformed Input" and nothing else ---------------------------

    static Stream<Arguments> malformed() {
        return Stream.of(
                Arguments.of("empty input", ""),
                Arguments.of("header without #", "job_id,runtime_in_seconds,next_job_id\n1,5,0\n"),
                Arguments.of("misspelled header", "#job_id,runtime,next_job_id\n1,5,0\n"),
                Arguments.of("no header, data first", "1,5,0\n2,5,0\n"),
                Arguments.of("too few fields", HEADER + "1,60\n"),
                Arguments.of("too many fields", HEADER + "1,60,0,7\n"),
                Arguments.of("trailing comma", HEADER + "1,60,\n"),
                Arguments.of("trailing comma after three fields", HEADER + "1,60,0,\n"),
                Arguments.of("empty field", HEADER + "1,,0\n"),
                Arguments.of("not a number", HEADER + "a,60,0\n"),
                Arguments.of("negative runtime", HEADER + "1,-5,0\n"),
                Arguments.of("explicit plus sign", HEADER + "1,+5,0\n"),
                Arguments.of("decimal runtime", HEADER + "1,6.5,0\n"),
                Arguments.of("space inside a field", HEADER + "1, 60,0\n"),
                Arguments.of("number beyond long", HEADER + "1,99999999999999999999,0\n"),
                Arguments.of("id 0 is the end marker", HEADER + "0,5,0\n"),
                Arguments.of("duplicate id", HEADER + "1,5,0\n1,7,0\n"),
                Arguments.of("next job does not exist", HEADER + "1,5,2\n"),
                Arguments.of("self loop", HEADER + "1,5,1\n"),
                Arguments.of("two-job cycle", HEADER + "1,5,2\n2,5,1\n"),
                Arguments.of("three-job cycle", HEADER + "1,5,2\n2,5,3\n3,5,1\n"),
                // "rho": a tail runs into a cycle; job 2 has two predecessors (1 and 3)
                Arguments.of("tail running into a cycle", HEADER + "1,5,2\n2,5,3\n3,5,2\n"),
                // a fork needs one job with two next ids, which the format can only express as a repeated id
                Arguments.of("fork written as a repeated id", HEADER + "1,5,2\n1,5,3\n2,5,0\n3,5,0\n"),
                Arguments.of("cycle beside a valid chain", HEADER + "1,5,0\n2,5,3\n3,5,2\n"),
                Arguments.of("two jobs before the same job", HEADER + "1,5,3\n2,5,3\n3,5,0\n"),
                // counting jobs alone is fooled here: job 3 is walked twice and the self loop 4 never, 4 == 4
                Arguments.of("shared job balanced by a self loop", HEADER + "1,5,3\n2,5,3\n3,5,0\n4,5,4\n"),
                Arguments.of("blank line between jobs", HEADER + "1,5,0\n\n2,5,0\n"),
                Arguments.of("malformed line after valid ones", HEADER + "1,5,0\n2,5,0\ngarbage\n"));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("malformed")
    void malformedInputPrintsOnlyTheError(String name, String input) {
        assertEquals(MALFORMED, run(input));
    }

    // ---- valid edge cases ---------------------------------------------------------------------------------------

    @Test
    void headerOnlyIsAnEmptyReport() {
        assertEquals("-\n", run(HEADER));
    }

    @Test
    void singleJobChain() {
        assertEquals("-\n" + section(7, 7, 1, "00:00:09", "00:00:09"), run(HEADER + "7,9,0\n"));
    }

    @Test
    void chainStartIsTheJobNobodyPointsToNotTheFirstLine() {
        String input = HEADER + "3,1,0\n2,1,3\n1,1,2\n";
        assertEquals("-\n" + section(1, 3, 3, "00:00:03", "00:00:01"), run(input));
    }

    @Test
    void equalRuntimesAreOrderedByStartJobAscending() {
        String input = HEADER + "9,10,0\n4,10,0\n6,10,0\n";
        assertEquals("-\n" + section(4, 4, 1, "00:00:10", "00:00:10") + section(6, 6, 1, "00:00:10", "00:00:10")
                + section(9, 9, 1, "00:00:10", "00:00:10"), run(input));
    }

    @Test
    void hoursMinutesSecondsAndTruncatedAverage() {
        // 3661 + 3600 = 7261 s = 02:01:01; average 3630.5 -> 3630 s = 01:00:30
        String input = HEADER + "1,3661,2\n2,3600,0\n";
        assertEquals("-\n" + section(1, 2, 2, "02:01:01", "01:00:30"), run(input));
    }

    @Test
    void moreThan99HoursKeepsAllDigits() {
        assertEquals("-\n" + section(1, 1, 1, "100:00:00", "100:00:00"), run(HEADER + "1,360000,0\n"));
    }

    @Test
    void zeroRuntimeIsValid() {
        assertEquals("-\n" + section(1, 2, 2, "00:00:00", "00:00:00"), run(HEADER + "1,0,2\n2,0,0\n"));
    }

    @Test
    void windowsLineEndingsAndTrailingBlankLinesAreAccepted() {
        String input = "#job_id,runtime_in_seconds,next_job_id\r\n1,60,0\r\n\r\n\n";
        assertEquals("-\n" + section(1, 1, 1, "00:01:00", "00:01:00"), run(input));
    }

    @Test
    void noTrailingNewlineAtEndOfInput() {
        assertEquals("-\n" + section(1, 1, 1, "00:01:00", "00:01:00"), run(HEADER + "1,60,0"));
    }

    @Test
    void idsLargerThanInt() {
        String input = HEADER + "4000000000,5,4000000001\n4000000001,5,0\n";
        assertEquals("-\n" + section(4_000_000_000L, 4_000_000_001L, 2, "00:00:10", "00:00:05"), run(input));
    }

    // ---- scale: a 100k-job chain listed in reverse (recursion would overflow the stack), and 50k short chains ---

    @Test
    void longChainListedBackwards() {
        int n = 100_000;
        String jobs = IntStream.iterate(n, i -> i >= 1, i -> i - 1)
                .mapToObj(i -> i + ",1," + (i == n ? 0 : i + 1))
                .collect(Collectors.joining("\n", HEADER, "\n"));
        String out = assertTimeoutPreemptively(Duration.ofSeconds(3), () -> run(jobs));
        assertEquals("-\n" + section(1, n, n, "27:46:40", "00:00:01"), out);
    }

    @Test
    void manyShortChains() {
        int chains = 50_000;
        String jobs = IntStream.rangeClosed(1, chains)
                .mapToObj(i -> (2 * i - 1) + "," + i + "," + (2 * i) + "\n" + (2 * i) + ",0,0")
                .collect(Collectors.joining("\n", HEADER, "\n"));
        String out = assertTimeoutPreemptively(Duration.ofSeconds(3), () -> run(jobs));
        String[] lines = out.split("\n");
        assertEquals(1 + 6 * chains, lines.length);
        assertEquals("start_job: " + (2 * chains - 1), lines[1], "longest chain first");
        assertEquals("start_job: 1", lines[lines.length - 6], "shortest chain last");
    }
}
