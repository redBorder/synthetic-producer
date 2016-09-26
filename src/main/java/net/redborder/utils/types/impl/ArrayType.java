package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ArrayType implements Type {
    Map<String, Type> types = new HashMap<>();

    public ArrayType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            Type type = TypeManager.newType(component.getValue());
            types.put(component.getKey(), type);
        }
    }

    @Override
    public Object get() {
        List<Object> array = new ArrayList<>();

        for (Map.Entry<String, Type> type : types.entrySet()) {
            array.add(type.getValue().get());
        }

        return array;
    }
}
