package headland;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class ToolchainTest {

    @Test
    void patternSwitchOverSealedRecords() {
        assertEquals(4.0, Toolchain.area(new Toolchain.Square(2.0)));
        assertEquals(Math.PI, Toolchain.area(new Toolchain.Circle(1.0)), 1e-12);
    }
}
