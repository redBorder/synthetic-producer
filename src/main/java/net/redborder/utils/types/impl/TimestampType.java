package net.redborder.utils.types.impl;

import net.redborder.utils.types.Type;

import java.util.Map;

public class TimestampType implements Type {
    public TimestampType(Map<String, Object> params) {}

    @Override
    public Object get() {
        return (System.currentTimeMillis() / 1000);
    }
}
