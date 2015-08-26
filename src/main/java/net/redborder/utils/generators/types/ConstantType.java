package net.redborder.utils.generators.types;

import java.util.Map;

public class ConstantType implements Type {
    private String constant;

    public ConstantType(Map<String, Object> params) {
        this.constant = String.valueOf(params.get("value"));
    }

    public ConstantType(String constant) {
        this.constant = constant;
    }

    @Override
    public Object get() {
        return constant;
    }
}
