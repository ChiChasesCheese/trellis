package headland;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicReference;

/** Test helpers: pick Starter or Solution from -Dimpl, and capture what a call prints to System.out. */
public final class Impl {

    private Impl() {}

    /** The static method {@code name} of {@code headland.<problem>.Starter|Solution}, chosen by -Dimpl. */
    public static Method staticMethod(String problem, String name, Class<?>... params) {
        String impl = System.getProperty("impl", "solution");
        String className = "headland." + problem + "." + Character.toUpperCase(impl.charAt(0)) + impl.substring(1);
        try {
            return Class.forName(className).getMethod(name, params);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("cannot load " + className + "." + name, e);
        }
    }

    /** Longest any single call may run; an infinite loop fails the test instead of hanging the whole build. */
    public static final Duration TIME_LIMIT = Duration.ofSeconds(5);

    /**
     * Invokes a static method on a daemon thread and returns everything it printed. System.out is restored even if
     * the call throws or runs past {@link #TIME_LIMIT}; a call still running then is abandoned (daemon threads do not
     * keep the JVM alive).
     */
    public static String stdoutOf(Method method, Object... args) {
        PrintStream original = System.out;
        var buffer = new ByteArrayOutputStream();
        var capture = new PrintStream(buffer, true, StandardCharsets.UTF_8);
        var thrown = new AtomicReference<Throwable>();
        Thread worker = Thread.ofPlatform().daemon().name("impl-under-test").unstarted(() -> {
            try {
                method.invoke(null, args);
            } catch (InvocationTargetException e) {
                thrown.set(e.getCause());
            } catch (IllegalAccessException e) {
                thrown.set(e);
            }
        });
        System.setOut(capture);
        try {
            worker.start();
            worker.join(TIME_LIMIT);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new AssertionError("interrupted while waiting for the implementation", e);
        } finally {
            System.setOut(original);
        }
        if (worker.isAlive()) {
            throw new AssertionError("did not finish within " + TIME_LIMIT.toSeconds() + " s: an infinite loop?");
        }
        if (thrown.get() != null) {
            throw new AssertionError("the implementation threw", thrown.get());
        }
        capture.flush();
        return buffer.toString(StandardCharsets.UTF_8);  // join() above makes the worker's writes visible here
    }

    /** Runs {@code main} of the chosen implementation with {@code stdin} as System.in; returns what it printed. */
    public static String runMain(String problem, String stdin) {
        Method main = staticMethod(problem, "main", String[].class);
        InputStream original = System.in;
        System.setIn(new ByteArrayInputStream(stdin.getBytes(StandardCharsets.UTF_8)));
        try {
            // the cast matters: a bare String[] would be spread into the Object... varargs as zero arguments
            return stdoutOf(main, (Object) new String[0]);
        } finally {
            System.setIn(original);
        }
    }
}
