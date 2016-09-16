package net.redborder.utils.types;

import java.util.Map;

public abstract class MappedType implements Type {

    public abstract Map<String, Object> getMap();

    @Override
    public Object get() {
        return getMap();
    }
}
