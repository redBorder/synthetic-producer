package net.redborder.utils.types;

import java.util.Map;

public class TimestampType implements Type {
    public TimestampType(Map<String, Object> params) {}

    @Override
    public Object get() {
        return (System.currentTimeMillis() / 1000);
    }
}
