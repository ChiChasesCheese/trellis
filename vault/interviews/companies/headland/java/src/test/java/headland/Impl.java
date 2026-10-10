package headland;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.charset.StandardCharsets;

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

    /** Invokes a static method and returns everything it printed; System.out is restored even if it throws. */
    public static String stdoutOf(Method method, Object... args) {
        PrintStream original = System.out;
        var buffer = new ByteArrayOutputStream();
        try (var capture = new PrintStream(buffer, true, StandardCharsets.UTF_8)) {
            System.setOut(capture);
            method.invoke(null, args);
        } catch (InvocationTargetException e) {
            throw new AssertionError("the implementation threw", e.getCause());
        } catch (IllegalAccessException e) {
            throw new IllegalStateException(e);
        } finally {
            System.setOut(original);
        }
        return buffer.toString(StandardCharsets.UTF_8);
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
