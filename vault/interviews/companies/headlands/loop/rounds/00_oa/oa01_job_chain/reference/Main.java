import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

/** HackerRank 形态：stdin → stdout。原题要求：非法输入也 exit zero，只打印 Malformed Input。 */
public class Main {
    public static void main(String[] args) {
        var in = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        var outcome = JobChains.analyze(in.lines().toList());
        JobChains.render(outcome).forEach(System.out::println);
    }
}
