package headland.q02;

import headland.q02.Solution.Chain;
import headland.q02.Solution.Job;
import headland.q02.Solution.MalformedInputException;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Job Runner written with streams throughout: same behaviour and tests as the imperative {@link Solution}, whose
 * {@code Job}, {@code Chain}, {@code HEADER} and {@code MalformedInputException} it reuses.
 *
 * <p>Run: {@code mvn -q test -Dimpl=functional -Dtest='headland/q02/**'}
 */
public final class Functional {

    /** A whole job line: three runs of digits, nothing else (no signs, spaces, decimals, empty or extra fields). */
    private static final Pattern JOB_LINE = Pattern.compile("(\\d+),(\\d+),(\\d+)");

    private static final Comparator<Chain> LONGEST_FIRST =
            Comparator.comparingLong(Chain::runtime).reversed().thenComparingLong(Chain::start);

    private Functional() {}

    public static void main(String[] args) throws IOException {
        var reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        List<String> lines = reader.lines().toList();
        String output;
        try {
            output = render(chains(parse(lines)));
        } catch (MalformedInputException e) {
            output = "Malformed Input\n";
        }
        System.out.print(output);
        System.out.flush();
    }

    static Map<Long, Job> parse(List<String> lines) throws MalformedInputException {
        // Java 21 List.reversed(): drop trailing blank lines from the end, then turn the view back around
        List<String> content = lines.reversed().stream().dropWhile(String::isBlank).toList().reversed();
        if (content.isEmpty() || !content.getFirst().strip().equals(Solution.HEADER)) {
            throw new MalformedInputException("missing or wrong header");
        }

        List<Optional<Job>> rows = content.stream().skip(1).map(Functional::toJob).toList();
        if (rows.stream().anyMatch(Optional::isEmpty)) {
            throw new MalformedInputException("a line is not three non-negative integers");
        }
        List<Job> jobs = rows.stream().map(Optional::orElseThrow).toList();

        if (jobs.stream().anyMatch(job -> job.id() == 0)) {
            throw new MalformedInputException("id 0 is reserved for 'end of chain'");
        }
        if (jobs.stream().map(Job::id).distinct().count() != jobs.size()) {
            throw new MalformedInputException("duplicate id");
        }
        return jobs.stream().collect(Collectors.toMap(
                Job::id, Function.identity(), (first, second) -> first, LinkedHashMap::new));  // no duplicates left
    }

    /** One line as a Job, or empty when it is not exactly three non-negative integers that fit in a long. */
    private static Optional<Job> toJob(String line) {
        Matcher fields = JOB_LINE.matcher(line.strip());
        if (!fields.matches()) {
            return Optional.empty();
        }
        try {
            return Optional.of(new Job(
                    Long.parseLong(fields.group(1)), Long.parseLong(fields.group(2)), Long.parseLong(fields.group(3))));
        } catch (NumberFormatException beyondLong) {
            return Optional.empty();
        }
    }

    static List<Chain> chains(Map<Long, Job> jobs) throws MalformedInputException {
        // job id -> how many jobs name it as their next
        Map<Long, Long> predecessors = jobs.values().stream()
                .map(Job::next)
                .filter(next -> next != 0)
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

        if (!jobs.keySet().containsAll(predecessors.keySet())) {
            throw new MalformedInputException("a next_job_id points to a missing job");
        }
        if (predecessors.values().stream().anyMatch(count -> count > 1)) {
            throw new MalformedInputException("two jobs run before the same job");
        }

        // safe to walk now: with at most one predecessor per job, no start can reach a cycle
        List<Chain> chains = jobs.values().stream()
                .filter(job -> !predecessors.containsKey(job.id()))
                .map(start -> walk(start, jobs))
                .sorted(LONGEST_FIRST)
                .toList();

        if (chains.stream().mapToLong(Chain::jobs).sum() != jobs.size()) {
            throw new MalformedInputException("a cycle: some jobs belong to no chain");
        }
        return chains;
    }

    /** Follows next ids from start. Ends because parse rejects id 0, so {@code jobs.get(0)} is null. */
    private static Chain walk(Job start, Map<Long, Job> jobs) {
        return Stream.iterate(start, Objects::nonNull, job -> jobs.get(job.next()))
                .collect(Collectors.teeing(
                        Collectors.reducing((earlier, later) -> later),
                        Collectors.summarizingLong(Job::runtime),
                        (last, stats) -> new Chain(start.id(), last.orElseThrow().id(),
                                Math.toIntExact(stats.getCount()), stats.getSum())));
    }

    static String render(List<Chain> chains) {
        // joining's prefix is written even for an empty stream, so a header-only log still prints "-"
        return chains.stream().map(Functional::section).collect(Collectors.joining("", "-\n", ""));
    }

    private static String section(Chain chain) {
        return """
                start_job: %d
                last_job: %d
                number_of_jobs: %d
                job_chain_runtime: %s
                average_job_time: %s
                -
                """.formatted(chain.start(), chain.last(), chain.jobs(),
                hhmmss(chain.runtime()), hhmmss(chain.averageRuntime()));
    }

    static String hhmmss(long seconds) {
        Duration d = Duration.ofSeconds(seconds);
        return "%02d:%02d:%02d".formatted(d.toHours(), d.toMinutesPart(), d.toSecondsPart());  // toHours is not a part
    }
}
