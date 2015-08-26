package net.redborder.utils.generators.types;

import java.util.Map;
import java.util.Random;

public class IntegerType implements Type {
    private Random randomGen = new Random();
    private Integer max, min;

    public IntegerType(Map<String, Object> params) {
        this.max = (Integer) params.get("max");
        this.min = (Integer) params.get("min");
        if (this.max == null) this.max = Integer.MAX_VALUE;
        if (this.min == null) this.min = 0;
    }

    @Override
    public Object get() {
        Integer rand = (randomGen.nextInt(max - min) + min);
        return rand;
    }
}
