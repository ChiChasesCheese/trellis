package headland;

/** Smoke check that the build really compiles Java 21: a sealed interface, records and a pattern switch. */
public final class Toolchain {

    public sealed interface Shape permits Circle, Square {}

    public record Circle(double radius) implements Shape {}

    public record Square(double side) implements Shape {}

    private Toolchain() {}

    public static double area(Shape shape) {
        return switch (shape) {
            case Circle c -> Math.PI * c.radius() * c.radius();
            case Square s -> s.side() * s.side();
        };
    }
}
