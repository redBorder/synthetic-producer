package net.redborder.utils.types;

import java.util.Map;

public class CounterType implements Type {
    private Integer max, min, counter;
    private Boolean direction;

    public CounterType(Map<String, Object> params) {
        this.max = (Integer) params.get("max");
        this.min = (Integer) params.get("min");
        this.direction = (Boolean) params.get("direction");
        if (this.max == null) this.max = Integer.MAX_VALUE;
        if (this.min == null) this.min = 0;
        if (this.direction == null) this.direction = true;
        if (this.min > this.max) this.max = this.min;
        if (direction) this.counter = this.min - 1; else this.counter = this.max + 1;
    }

    @Override
    public Object get() {
        if (direction)
        {
            if (counter < max)
                counter++;
            else if (counter.equals(max))
                counter = min;
        }
        else
        {    if (counter > min)
                counter--;
            else if (counter.equals(min))
                counter = max;
        }
        return counter;
    }
}
