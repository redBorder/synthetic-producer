package net.redborder.utils.types.impl;

import net.redborder.utils.types.Type;

import java.util.Map;
import java.util.Random;

public class DoubleType implements Type {
    private Double max, min;
    private Integer truncate;

    public DoubleType(Map<String, Object> params) {
        this.max = (Double) params.get("max");
        this.min = (Double) params.get("min");
        this.truncate = (Integer) params.get("truncate");
        if(truncate == null) truncate = 10000;
        if (this.max == null) this.max = Double.MAX_VALUE;
        else this.max += 1;
        if (this.min == null) this.min = 0.00d;
    }

    @Override
    public Object get() {
        if (!max.equals(min)) {
            return Math.floor((min + (Math.random() * (max - min))) * truncate) / truncate;
        } else {
            return max;
        }
    }
}
