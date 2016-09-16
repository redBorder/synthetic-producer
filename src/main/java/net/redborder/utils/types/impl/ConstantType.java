package net.redborder.utils.types.impl;

import net.redborder.utils.types.Type;

import java.util.Map;

public class ConstantType implements Type {
    private Object constant;

    public ConstantType(Map<String, Object> params) {
        this.constant = params.get("value");
    }

    public ConstantType(Object constant) {
        this.constant = constant;
    }

    @Override
    public Object get() {
        return constant;
    }
}
