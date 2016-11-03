package net.redborder.utils.types.impl;

import net.redborder.utils.types.MappedType;
import net.redborder.utils.types.Type;
import net.redborder.utils.types.TypeManager;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class JsonType implements Type {
    Map<String, Type> types = new HashMap<>();

    public JsonType(Map<String, Object> params) {
        Map<String, Map<String, Object>> components = (Map<String, Map<String, Object>>) params.get("components");

        for (Map.Entry<String, Map<String, Object>> component : components.entrySet()) {
            Type type = TypeManager.newType(component.getValue());
            types.put(component.getKey(), type);
        }
    }

    @Override
    public Object get() {
        Map<String, Object> typeValue = new HashMap<>();

        for (Map.Entry<String, Type> type : types.entrySet()) {
            if (type.getValue() instanceof MappedType) {
                typeValue.putAll((Map<String, Object>) type.getValue().get());
            } else {
                typeValue.put(type.getKey(), type.getValue().get());
            }
        }

        return typeValue;
    }
}
