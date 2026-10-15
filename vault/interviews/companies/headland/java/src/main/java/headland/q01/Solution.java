package headland.q01;

/** Reference: the body of HackerRank's {@code Result.fizzBuzz}. */
public final class Solution {

    private Solution() {}

    public static void fizzBuzz(int n) {
        var out = new StringBuilder(n * 5);
        for (int i = 1; i <= n; i++) {
            String line;
            if (i % 15 == 0) {
                line = "FizzBuzz";
            } else if (i % 3 == 0) {
                line = "Fizz";
            } else if (i % 5 == 0) {
                line = "Buzz";
            } else {
                line = String.valueOf(i);
            }
            out.append(line).append('\n');
        }
        System.out.print(out);
        System.out.flush();
    }
}
