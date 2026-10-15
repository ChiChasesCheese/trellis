package headland.q01;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTimeoutPreemptively;

import headland.Impl;
import java.lang.reflect.Method;
import java.time.Duration;
import java.util.List;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class FizzBuzzTest {

    private static final Method FIZZ_BUZZ = Impl.staticMethod("q01", "fizzBuzz", int.class);

    private static List<String> run(int n) {
        return Impl.stdoutOf(FIZZ_BUZZ, n).lines().toList();
    }

    /** Independent oracle, written the obvious way. */
    private static String expected(int i) {
        if (i % 15 == 0) return "FizzBuzz";
        if (i % 3 == 0) return "Fizz";
        if (i % 5 == 0) return "Buzz";
        return String.valueOf(i);
    }

    @Test
    void statementExample() {
        assertEquals(
                List.of("1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                        "11", "Fizz", "13", "14", "FizzBuzz"),
                run(15));
    }

    @Test
    void smallestInput() {
        assertEquals(List.of("1"), run(1));
    }

    @ParameterizedTest(name = "n = {0}: last line is {1}")
    @CsvSource({"3, Fizz", "5, Buzz", "15, FizzBuzz", "30, FizzBuzz", "31, 31", "45, FizzBuzz", "99, Fizz", "100, Buzz"})
    void lastLineIsTheValueForN(int n, String last) {
        List<String> lines = run(n);
        assertEquals(n, lines.size(), "exactly one line per i in 1..n");
        assertEquals(last, lines.getLast());
    }

    @Test
    void exactTextNoPaddingOrCaseChanges() {
        String out = Impl.stdoutOf(FIZZ_BUZZ, 15);
        assertEquals(15, out.lines().count(), "one line per i");
        assertEquals(String.join("\n", run(15)), out.strip().replace("\r\n", "\n"),
                "no blank lines, no trailing spaces");
        for (String line : run(15)) {
            assertEquals(line.strip(), line, "no leading or trailing whitespace on '" + line + "'");
        }
    }

    @Test
    void largestInputMatchesOracleWithinTimeLimit() {
        int n = 199_999;  // constraint: 0 < n < 2 * 10^5
        List<String> lines = assertTimeoutPreemptively(Duration.ofSeconds(2), () -> run(n));
        assertEquals(n, lines.size());
        List<String> want = IntStream.rangeClosed(1, n).mapToObj(FizzBuzzTest::expected).toList();
        assertEquals(want, lines);
    }
}
