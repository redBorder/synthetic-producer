package net.redborder.utils.types;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

import java.util.HashMap;
import java.util.Map;

@RunWith(MockitoJUnitRunner.class)
public class IntegerTypeTest extends TestCase {
    @Test
    public void get() {
        Integer MAX = 67;
        Integer MIN = 0;

        Map<String, Object> opts = new HashMap<>();
        opts.put("max", MAX);
        opts.put("min", MIN);

        IntegerType type = new IntegerType(opts);
        for (int i = 0; i < 999; i++) {
            Integer result = (Integer) type.get();
            if (result > MAX || result < MIN) {
                fail("Integer range violated");
            }
        }
    }
}
