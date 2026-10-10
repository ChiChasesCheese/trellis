package headland.q02;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

/** Reference: HackerRank's {@code Solution} for Job Runner. Parse everything, validate everything, then print. */
public final class Solution {

    static final String HEADER = "#job_id,runtime_in_seconds,next_job_id";

    /** Digits only: rejects signs, spaces, decimals and empty fields before parsing. */
    private static final Pattern NON_NEGATIVE_INTEGER = Pattern.compile("\\d+");

    record Job(long id, long runtime, long next) {}

    record Chain(long start, long last, int jobs, long runtime) {
        long averageRuntime() {
            return runtime / jobs;  // truncates: 35 s over 2 jobs -> 17 s, as in the example
        }
    }

    static final class MalformedInputException extends Exception {
        private static final long serialVersionUID = 1L;  // Exception is Serializable; -Xlint asks for this

        MalformedInputException(String reason) {
            super(reason);
        }
    }

    private Solution() {}

    public static void main(String[] args) throws IOException {
        // not try-with-resources: closing this reader would close System.in
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

    /** Header check, then one Job per line, keyed by id in input order. */
    static Map<Long, Job> parse(List<String> lines) throws MalformedInputException {
        int end = lines.size();
        while (end > 0 && lines.get(end - 1).isBlank()) {
            end--;  // trailing blank lines end the file; a blank line between jobs is still malformed
        }
        if (end == 0 || !lines.get(0).strip().equals(HEADER)) {
            throw new MalformedInputException("missing or wrong header");
        }
        var jobs = new LinkedHashMap<Long, Job>();
        for (String line : lines.subList(1, end)) {
            String[] fields = line.strip().split(",", -1);  // -1 keeps trailing empty fields: "1,60," has 3
            if (fields.length != 3) {
                throw new MalformedInputException("expected 3 fields: " + line);
            }
            var job = new Job(number(fields[0]), number(fields[1]), number(fields[2]));
            if (job.id() == 0) {
                throw new MalformedInputException("id 0 is reserved for 'end of chain'");
            }
            if (jobs.putIfAbsent(job.id(), job) != null) {
                throw new MalformedInputException("duplicate id " + job.id());
            }
        }
        return jobs;
    }

    private static long number(String field) throws MalformedInputException {
        if (!NON_NEGATIVE_INTEGER.matcher(field).matches()) {
            throw new MalformedInputException("not a non-negative integer: '" + field + "'");
        }
        try {
            return Long.parseLong(field);
        } catch (NumberFormatException e) {
            throw new MalformedInputException("out of range: " + field);
        }
    }

    /** Links jobs into chains; every job must sit on exactly one straight chain that ends in 0. */
    static List<Chain> chains(Map<Long, Job> jobs) throws MalformedInputException {
        Set<Long> hasPredecessor = new HashSet<>();
        for (Job job : jobs.values()) {
            if (job.next() == 0) {
                continue;
            }
            if (!jobs.containsKey(job.next())) {
                throw new MalformedInputException("job " + job.id() + " points to missing job " + job.next());
            }
            if (!hasPredecessor.add(job.next())) {
                throw new MalformedInputException("two jobs run before job " + job.next());
            }
        }

        var chains = new ArrayList<Chain>();
        int jobsOnChains = 0;
        for (Job first : jobs.values()) {
            if (hasPredecessor.contains(first.id())) {
                continue;  // not a start
            }
            Job job = first;
            int count = 1;
            long runtime = job.runtime();
            while (job.next() != 0) {  // terminates: no job has two predecessors, so a start never reaches a cycle
                job = jobs.get(job.next());
                count++;
                runtime += job.runtime();
            }
            chains.add(new Chain(first.id(), job.id(), count, runtime));
            jobsOnChains += count;
        }
        if (jobsOnChains != jobs.size()) {
            throw new MalformedInputException("a cycle: some jobs belong to no chain");
        }

        chains.sort(Comparator.comparingLong(Chain::runtime).reversed().thenComparingLong(Chain::start));
        return chains;
    }

    static String render(List<Chain> chains) {
        var out = new StringBuilder("-\n");
        for (Chain chain : chains) {
            out.append("""
                    start_job: %d
                    last_job: %d
                    number_of_jobs: %d
                    job_chain_runtime: %s
                    average_job_time: %s
                    -
                    """.formatted(chain.start(), chain.last(), chain.jobs(),
                    hhmmss(chain.runtime()), hhmmss(chain.averageRuntime())));
        }
        return out.toString();
    }

    static String hhmmss(long seconds) {
        return "%02d:%02d:%02d".formatted(seconds / 3600, seconds % 3600 / 60, seconds % 60);
    }
}
