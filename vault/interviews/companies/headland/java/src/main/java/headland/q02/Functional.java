package headland.q02;

import headland.q02.Solution.Chain;
import headland.q02.Solution.Job;
import headland.q02.Solution.MalformedInputException;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Job Runner with a stream-based {@code chains}; {@code parse} and {@code render} are reused from {@link Solution}.
 *
 * <p>Run: {@code mvn -q test -Dimpl=functional -Dtest='headland/q02/**'}
 */
public final class Functional {

    private static final Comparator<Chain> LONGEST_FIRST =
            Comparator.comparingLong(Chain::runtime).reversed().thenComparingLong(Chain::start);

    private Functional() {}

    public static void main(String[] args) throws IOException {
        var reader = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        List<String> lines = reader.lines().toList();
        String output;
        try {
            output = Solution.render(chains(Solution.parse(lines)));
        } catch (MalformedInputException e) {
            output = "Malformed Input\n";
        }
        System.out.print(output);
        System.out.flush();
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
}
