package net.redborder.utils.types;

import junit.framework.TestCase;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

import java.util.HashMap;
import java.util.Map;

@RunWith(MockitoJUnitRunner.class)
public class MacTypeTest extends TestCase {
    @Test
    public void get() {
        String MIN = "00:00:00:00:00:00";
        String MAX = "00:00:00:00:00:FF";
        long minLong = MacType.longFromMac(MIN);
        long maxLong = MacType.longFromMac(MAX);

        Map<String, Object> opts = new HashMap<>();
        opts.put("max", MAX);
        opts.put("min", MIN);

        MacType type = new MacType(opts);
        for (int i = 0; i < 999; i++) {
            String result = (String) type.get();
            long resultLong = MacType.longFromMac(result);

            if (resultLong >= maxLong || resultLong < minLong) {
                fail("Mac range violated");
            }
        }
    }
}
